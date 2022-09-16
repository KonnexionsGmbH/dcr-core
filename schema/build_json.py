import json
import xml.etree.ElementTree as ET
import re
from collections import defaultdict
from pathlib import Path

obj = {}

tree = ET.parse('all_clauses.line.xml')
root = tree.getroot()
namespace = re.match(r'\{.*\}', root.tag).group(0)
creation = root.find(f'{namespace}Creation')

obj['processed'] = creation.attrib['date']

document = root.find(f'{namespace}Document')

obj['file_name'] = Path(document.attrib['filename']).name
obj['page_count'] = Path(document.attrib['pageCount']).name
obj['file_size'] = Path(document.attrib['filesize']).name

obj['author'] = document.findtext(f'{namespace}DocInfo/{namespace}Author')
obj['created'] = document.findtext(f'{namespace}DocInfo/{namespace}CreationDate')

pages = document.find(f'{namespace}Pages')
resources = pages.find(f'{namespace}Resources')


def attr_to_json(target_obj, obj_key, root_elm, elm):
    target_obj[obj_key] = defaultdict(dict)
    _id = None
    for child in root_elm.find(f'{namespace}{elm}'):
        for key, value in child.attrib.items():
            if key == 'id':
                _id = value
            else:
                target_obj[obj_key][_id][key] = value
    target_obj[obj_key] = dict(target_obj[obj_key])


attr_to_json(obj, 'fonts', resources, 'Fonts')
attr_to_json(obj, 'color_spaces', resources, 'ColorSpaces')

obj['pages'] = [
    {
        'attributes': {**page.attrib, **page.find(f'{namespace}Content').attrib},
        'paragraphs': [
            {
                'attributes': para.find(f'{namespace}Box').attrib,
                'lines': [
                    {
                        'attributes': line.attrib,
                        'text': text.text
                    }
                ]
            }
            for para in page.find(f'{namespace}Content')
            for line in para.find(f'{namespace}Box')
            for text in line
        ]
    }
    for page in document.find(f'{namespace}Pages') if page.tag == f'{namespace}Page'
]

with open("all_clauses.json", "w") as f:
    json.dump(obj, f, indent=1)
