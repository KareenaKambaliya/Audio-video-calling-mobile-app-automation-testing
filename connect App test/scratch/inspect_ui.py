import xml.etree.ElementTree as ET

tree = ET.parse('scratch_login_source.xml')
root = tree.getroot()

print("--- ALL MATCHING ELEMENTS ---")
for elem in root.iter():
    text = elem.attrib.get('text', '')
    res_id = elem.attrib.get('resource-id', '')
    cls = elem.attrib.get('class', '')
    clickable = elem.attrib.get('clickable', '')
    bounds = elem.attrib.get('bounds', '')
    content_desc = elem.attrib.get('content-desc', '')
    lower_str = (text + " " + res_id + " " + content_desc).lower()
    if any(k in lower_str for k in ['login', 'sign', 'button', 'kareena', 'edt', 'btn']):
        print(f"Tag: {elem.tag} | Class: {cls}")
        print(f"  ResID: {res_id}")
        print(f"  Text: '{text}' | Desc: '{content_desc}'")
        print(f"  Clickable: {clickable} | Bounds: {bounds}")
        print("-" * 50)
