import zipfile
import struct

apk_path = r'data/Connect_mobile_ss.apk'

def extract_strings_from_axml(axml_bytes):
    header_type, header_size, file_size = struct.unpack('<HHI', axml_bytes[:8])
    pos = 8
    strings = []
    while pos < len(axml_bytes):
        chunk_type, chunk_header_size, chunk_size = struct.unpack('<HHI', axml_bytes[pos:pos+8])
        if chunk_type == 0x0001:
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
            break
        pos += chunk_size
    return strings

with zipfile.ZipFile(apk_path, 'r') as z:
    for name in z.namelist():
        if name.startswith('res/layout/') and name.endswith('.xml'):
            data = z.read(name)
            strs = extract_strings_from_axml(data)
            str_lower = [s.lower() for s in strs]
            if any('join with code' in s or 'welcome to' in s or 'login with' in s for s in str_lower):
                print(f"FOUND MATCH in: {name}!")
                for s in strs:
                    print("  ", s)
            # Also check for login button ID
            if any('btnlogin' in s or 'btn_login' in s or 'loginbutton' in s for s in str_lower):
                print(f"FOUND LOGIN BTN in: {name}!")
                for s in strs:
                    print("   [BTN]", s)
