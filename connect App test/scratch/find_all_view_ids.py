import zipfile
import re

with zipfile.ZipFile(r'data/Connect_mobile_ss.apk', 'r') as z:
    data = z.read('classes8.dex')
    # Find all identifiers around pos 520958 or starting with edt/et/txt/btn
    matches = re.findall(rb'(?:btn_|edt_|et_|txt_)[a-zA-Z0-9_]+', data)
    print("Unique matches:")
    for m in sorted(set(matches)):
        print(" ", m.decode())
