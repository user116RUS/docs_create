import zipfile
import re
import os

docx_path = 'c:/Users/User/dev/docs_create/main/document_templates/dogovor.docx'
output_path = 'c:/Users/User/dev/docs_create/main/document_templates/dogovor_fixed.docx'

def fix_docx_xml(input_file, output_file):
    with zipfile.ZipFile(input_file, 'r') as zin:
        with zipfile.ZipFile(output_file, 'w') as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    xml_content = content.decode('utf-8')
                    # Fix broken {% for row in services %} which appears as {% for row in services% ... }
                    # This is a bit risky but let's try to find the split tag.
                    # Looking at the output: {% for row in services% </w:t> ... <w:t>} {{loop.index}}
                    
                    # Pattern 1: Split for loop tag
                    xml_content = xml_content.replace('{% for row in services%</w:t>', '{% for row in services %}</w:t>')
                    xml_content = xml_content.replace('<w:t>}{{loop.index}}', '<w:t>{{loop.index}}')
                    
                    content = xml_content.encode('utf-8')
                zout.writestr(item, content)

fix_docx_xml(docx_path, output_path)
# Replace original with fixed
os.replace(output_path, docx_path)
print("Fixed dogovor.docx")
