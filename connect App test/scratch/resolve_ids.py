import zipfile
import struct

with zipfile.ZipFile(r'data/Connect_mobile_ss.apk', 'r') as z:
    arsc = z.read('resources.arsc')

# Find string pool of key names
# In ARSC format:
# TableHeader (12 bytes)
# PackageHeader
# TypeStrings pool
# KeyStrings pool
# TypeSpecs and Types

# Let's search for 'btn_reg' position
pos = arsc.find(b'btn_reg\x00')
print("Position of btn_reg:", pos)

# Let's print all identifiers in that key strings pool!
# Find where the pool starts (backward search for string pool header 0x0001)
p = pos
while p > 0:
    chunk_type = struct.unpack('<H', arsc[p:p+2])[0]
    if chunk_type == 0x0001:
        print(f"Found string pool chunk at {p}")
        break
    p -= 1

# Let's parse strings from this pool
if p > 0:
    header_type, header_size, chunk_size = struct.unpack('<HHI', arsc[p:p+8])
    string_count, style_count, flags, strings_start, styles_start = struct.unpack('<IIIII', arsc[p+8:p+28])
    is_utf8 = bool(flags & (1 << 8))
    offsets = struct.unpack(f'<{string_count}I', arsc[p+28:p+28+string_count*4])
    pool_start = p + strings_start
    key_strings = []
    for off in offsets:
        str_pos = pool_start + off
        if is_utf8:
            u16len = arsc[str_pos]
            str_pos += 1
            if u16len & 0x80: str_pos += 1
            u8len = arsc[str_pos]
            str_pos += 1
            if u8len & 0x80:
                u8len = ((u8len & 0x7F) << 8) | arsc[str_pos]
                str_pos += 1
            s = arsc[str_pos:str_pos+u8len].decode('utf-8', errors='replace')
        else:
            u16len = struct.unpack('<H', arsc[str_pos:str_pos+2])[0]
            str_pos += 2
            s = arsc[str_pos:str_pos+u16len*2].decode('utf-16le', errors='replace')
        key_strings.append(s)
    print(f"Extracted {len(key_strings)} key strings!")
    
    # Now let's find the entry in type 0x0a (id)
    # Target entry IDs:
    # 0x7f0a0094: entry index 0x0094 = 148
    # 0x7f0a010b: entry index 0x010b = 267
    # 0x7f0a010d: entry index 0x010d = 269
    # 0x7f0a04c4: entry index 0x04c4 = 1220
    # 0x7f0a04c5: entry index 0x04c5 = 1221
    
    print("\n--- RESOLVED RESOURCE IDS ---")
    entries = {
        0x0094: "PtmButton (Login Button)",
        0x010b: "PtmEditText 1 (Email)",
        0x0101: "PtmEditText 2",
        0x010d: "PtmEditText 3 (Password)",
        0x04c4: "PtmTextView (Join with Code)",
        0x04c5: "PtmTextView (Forgot Password)",
        0x044c: "PtmTextView (Subtitle)",
    }
    for e_idx, desc in entries.items():
        if e_idx < len(key_strings):
            print(f"ID 0x7f0a{e_idx:04x} -> {key_strings[e_idx]} ({desc})")
        else:
            print(f"ID 0x7f0a{e_idx:04x} -> OUT OF BOUNDS ({e_idx} >= {len(key_strings)})")
