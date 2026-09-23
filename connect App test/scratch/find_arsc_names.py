import zipfile
import struct

target_res_ids = {
    0x7f0a0094: 'Button',
    0x7f0a010b: 'EditText 1',
    0x7f0a0101: 'EditText 2',
    0x7f0a010d: 'EditText 3',
    0x7f0a04c4: 'Join Code',
    0x7f0a04c5: 'Forgot Password',
}

with zipfile.ZipFile(r'data/Connect_mobile_ss.apk', 'r') as z:
    arsc = z.read('resources.arsc')

# Find string in ARSC that corresponds to these entry names
# In resources.arsc, type 0x0a is 'id'.
# Let's search for string table chunks
pos = 0
header_type, header_size, file_size = struct.unpack('<HHI', arsc[:8])
print(f"Header: {header_type}, {header_size}, {file_size}")

# Search for the string pool that contains resource entry names
# Let's search for 'btnLogin' or 'btn_login' or 'btn' or 'txt' in the arsc
for target in [b'login', b'register', b'join', b'forgot']:
    matches = [m for m in range(len(arsc)) if arsc.startswith(target, m)]
    print(f"Target '{target.decode()}': found {len(matches)} times")
    for m in matches[:10]:
        # print string around m
        s = arsc[max(0, m-20):m+40]
        # try to get null-terminated string
        print("  ", s)
