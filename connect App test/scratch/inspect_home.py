import xml.etree.ElementTree as ET
tree = ET.parse('scratch_login_source.xml')
for elem in tree.getroot().iter():
    res = elem.attrib.get('resource-id', '')
    txt = elem.attrib.get('text', '')
    desc = elem.attrib.get('content-desc', '')
    cls = elem.attrib.get('class', '')
    if res or txt or desc:
        print(f'{cls} | ID: {res} | Text: "{txt}" | Desc: "{desc}"')
