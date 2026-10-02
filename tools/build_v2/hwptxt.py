import olefile, zlib, struct, sys, io, os

CTRL_INLINE = set([4,5,6,7,8,9,19,20])   # inline controls consuming 1 wchar... handled below

def para_text(payload):
    # payload is UTF-16LE stream with control chars
    out = []
    i = 0
    n = len(payload)
    while i + 1 < n:
        c = struct.unpack_from('<H', payload, i)[0]
        if c in (0,10,13):
            out.append('\n' if c in (10,13) else '')
            i += 2
        elif c in (1,2,3,11,12,14,15,16,17,18,21,22,23):
            i += 16   # extended control: 8 wchars
        elif c in (4,5,6,7,8,9,19,20):
            i += 2    # inline control
        else:
            out.append(chr(c))
            i += 2
    return ''.join(out)

def extract(path):
    f = olefile.OleFileIO(path)
    hdr = f.openstream('FileHeader').read()
    flags = struct.unpack_from('<I', hdr, 36)[0]
    compressed = bool(flags & 1)
    texts = []
    streams = [s for s in f.listdir() if s[0] in ('BodyText','ViewText')]
    order = sorted(set(tuple(s) for s in streams), key=lambda s: (s[0], int(''.join(ch for ch in s[1] if ch.isdigit()) or 0)))
    for s in order:
        data = f.openstream(list(s)).read()
        if compressed:
            try: data = zlib.decompress(data, -15)
            except Exception: continue
        i = 0
        while i + 4 <= len(data):
            h = struct.unpack_from('<I', data, i)[0]
            tag = h & 0x3FF
            size = (h >> 20) & 0xFFF
            i += 4
            if size == 0xFFF:
                size = struct.unpack_from('<I', data, i)[0]; i += 4
            body = data[i:i+size]; i += size
            if tag == 67:   # HWPTAG_PARA_TEXT
                texts.append(para_text(body))
            elif tag == 66: # HWPTAG_PARA_HEADER -> paragraph break
                texts.append('\n')
    f.close()
    return ''.join(texts)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    t = extract(src)
    io.open(dst, 'w', encoding='utf-8').write(t)
    print(os.path.basename(src), len(t))
