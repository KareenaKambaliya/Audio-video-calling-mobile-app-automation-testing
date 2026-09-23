import zipfile
import re

target_ids = {
    0x7f0a04bc: 'txt_contactname / name?',
    0x7f0a04bd: 'txt_contactnumber / role / email?',
    0x7f0a01f8: 'video call icon?',
    0x7f0a01fb: 'audio call icon?',
    0x7f0a0277: 'linear layout action?',
    0x7f0a0275: 'linear layout action 2?',
    0x7f0a0391: 'search view',
    0x7f0a032c: 'recycler view',
}

# In classes8.dex, R$id contains field definitions.
# Let's search classes8.dex for field names
with zipfile.ZipFile(r'data/Connect_mobile_ss.apk', 'r') as z:
    dex = z.read('classes8.dex')
    # Let's search for the R$id class in dex
    # All static fields of R$id are defined with IDs
    # Let's search for known strings like txt_contactname, txt_contactnumber
    for word in [b'txt_contactname', b'txt_contactnumber', b'img_contacts', b'llcontacts', b'search', b'contact', b'rv_']:
        matches = [m.start() for m in re.finditer(re.escape(word), dex)]
        print(f"Word '{word.decode()}': found {len(matches)} times")
        for m in matches[:3]:
            print("  context:", dex[max(0, m-20):min(len(dex), m+40)])
