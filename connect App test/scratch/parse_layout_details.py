import zipfile
import struct

apk_path = r'data/Connect_mobile_ss.apk'

def parse_axml_full(axml_bytes):
    # Parse Android Binary XML with tags and attributes
    header_type, header_size, file_size = struct.unpack('<HHI', axml_bytes[:8])
    pos = 8
    strings = []
    res_ids = []
    elements = []
    
    while pos < len(axml_bytes):
        chunk_type, chunk_header_size, chunk_size = struct.unpack('<HHI', axml_bytes[pos:pos+8])
        if chunk_type == 0x0001: # STRING POOL
            string_count, style_count, flags, strings_start, styles_start = struct.unpack('<IIIII', axml_bytes[pos+8:pos+28])
            is_utf8 = bool(flags & (1 << 8))
            offsets = struct.unpack(f'<{string_count}I', axml_bytes[pos+28:pos+28+string_count*4])
            pool_start = pos + strings_start
            for off in offsets:
                str_pos = pool_start + off
                if is_utf8:
                    u16len = axml_bytes[str_pos]
                    str_pos += 1
                    if u16len & 0x80: str_pos += 1
                    u8len = axml_bytes[str_pos]
                    str_pos += 1
                    if u8len & 0x80:
                        u8len = ((u8len & 0x7F) << 8) | axml_bytes[str_pos]
                        str_pos += 1
                    s = axml_bytes[str_pos:str_pos+u8len].decode('utf-8', errors='replace')
                else:
                    u16len = struct.unpack('<H', axml_bytes[str_pos:str_pos+2])[0]
                    str_pos += 2
                    if u16len & 0x8000:
                        u16len = ((u16len & 0x7FFF) << 16) | struct.unpack('<H', axml_bytes[str_pos:str_pos+2])[0]
                        str_pos += 2
                    s = axml_bytes[str_pos:str_pos+u16len*2].decode('utf-16le', errors='replace')
                strings.append(s)
        elif chunk_type == 0x0180: # RESOURCE MAP
            count = (chunk_size - 8) // 4
            res_ids = list(struct.unpack(f'<{count}I', axml_bytes[pos+8:pos+chunk_size]))
        elif chunk_type == 0x0102: # START TAG
            # line_number, comment, ns, name, attr_start, attr_size, attr_count, id_index, class_index, style_index
            tag_data = struct.unpack('<IIIIHHHHHH', axml_bytes[pos+8:pos+36])
            tag_name_idx = tag_data[3]
            tag_name = strings[tag_name_idx] if tag_name_idx < len(strings) else 'UNKNOWN'
            attr_count = tag_data[6]
            attrs = {}
            attr_pos = pos + 36
            for _ in range(attr_count):
                ans, aname_idx, aval_raw_idx, atype, adata = struct.unpack('<IIIIi', axml_bytes[attr_pos:attr_pos+20])
                aname = strings[aname_idx] if aname_idx < len(strings) else f'attr_{aname_idx}'
                aval = strings[aval_raw_idx] if (aval_raw_idx < len(strings) and aval_raw_idx >= 0) else str(adata)
                attrs[aname] = (aval, adata)
                attr_pos += 20
            elements.append((tag_name, attrs))
        pos += chunk_size
    return strings, res_ids, elements

with zipfile.ZipFile(apk_path, 'r') as z:
    for layout_name in ['res/layout/activity_register.xml']:
        strs, res_ids, elems = parse_axml_full(z.read(layout_name))
        print(f"=== {layout_name} Elements ===")
        for tag, attrs in elems:
            print(f"Tag: {tag}")
            for k, v in attrs.items():
                if k in ['id', 'text', 'hint', 'tag', 'src']:
                    print(f"   {k} = {v}")
