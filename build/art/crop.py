"""
Crop a rasterised icon to its own alpha bounds and write it back.

Pure stdlib on purpose: this repo has no Python dependencies and is not going
to grow one for a step that runs when an icon changes. PNG here is always
8-bit RGBA (that is what the headless-Chromium screenshot produces with
--default-background-color=00000000), so the reader below only handles that
case and says so loudly rather than guessing.

Why crop at all: Chromium renders the SVG at its natural size inside whatever
window it is given, so the capture is the WINDOW, not the artwork - padded, and
clipped outright if the window is the same size as the art. So we render into a
deliberately oversized window and cut the art back out here. It also matches
the client's own 3D icons, which are trimmed to their content (voucher-3d.png
is 256x186, not a padded square), so a wrapper sizing one of ours gets the same
optical weight as one of theirs.
"""
import struct
import sys
import zlib


def _unfilter(raw, w, h):
    stride = w * 4
    out = []
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        f = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if f == 1:
            for x in range(4, stride):
                line[x] = (line[x] + line[x - 4]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - 4] if x >= 4 else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - 4] if x >= 4 else 0
                b = prev[x]
                c = prev[x - 4] if x >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        elif f != 0:
            raise ValueError("unknown PNG filter %d" % f)
        out.append(bytes(line))
        prev = line
    return out


def read_rgba(path):
    d = open(path, "rb").read()
    pos, idat, w, h = 8, b"", 0, 0
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        data = d[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", data[:10])
            if (depth, ctype) != (8, 6):
                raise SystemExit("%s is not 8-bit RGBA (depth %d, colour type %d)" % (path, depth, ctype))
        elif typ == b"IDAT":
            idat += data
    return w, h, _unfilter(zlib.decompress(idat), w, h)


def write_rgba(path, w, h, rows):
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    open(path, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main(src, dst, pad=6):
    w, h, rows = read_rgba(src)
    xs, ys = [], []
    for y, r in enumerate(rows):
        for x in range(w):
            if r[x * 4 + 3]:
                xs.append(x)
                ys.append(y)
                break
        else:
            continue
        # rightmost opaque pixel on this row
        for x in range(w - 1, -1, -1):
            if r[x * 4 + 3]:
                xs.append(x)
                break
    if not xs:
        raise SystemExit("%s is fully transparent - the render failed" % src)
    x0, x1 = max(0, min(xs) - pad), min(w - 1, max(xs) + pad)
    y0, y1 = max(0, min(ys) - pad), min(h - 1, max(ys) + pad)
    cw, ch = x1 - x0 + 1, y1 - y0 + 1
    write_rgba(dst, cw, ch, [r[x0 * 4:(x1 + 1) * 4] for r in rows[y0:y1 + 1]])
    print("%s -> %dx%d" % (dst, cw, ch))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
