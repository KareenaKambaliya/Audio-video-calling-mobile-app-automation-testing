import zipfile
import re

with zipfile.ZipFile(r'data/Connect_mobile_ss.apk', 'r') as z:
    for dex_name in z.namelist():
        if dex_name.endswith('.dex'):
            data = z.read(dex_name)
            if b'Lcom/plutomen/ARMS/R$id;' in data:
                print(f"Found R$id in {dex_name}!")
                # Let's search for btn_reg, btnLogin, txt_guestlogin, etc.
                for word in [b'btn_reg', b'btn_login', b'btnLogin', b'txt_guestlogin', b'txt_forgotpwd', b'btn_join']:
                    idx = data.find(word)
                    print(f"  Word {word}: {idx}")
