import zipfile
import re
import os

docx_path = 'c:/Users/User/dev/docs_create/main/document_templates/dogovor.docx'

def find_jinja_tags(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('word/document.xml').decode('utf-8')
        
        # Find everything between {{ and }} or {% and %}
        tags = re.findall(r'(\{\{.*?\}\}|\{\%.*?\%\}|[\{\}])', content)
        
        for i, tag in enumerate(tags):
            print(f"{i}: {tag}")

        # Specifically look for common mistakes like { } or {{ } }
        # Or look at context around line 91 (approximate)
        print("\nFull XML (Snippet around suspect area):")
        # Line numbers in XML are not the same as Jinja2 line numbers
        # But let's look for suspicious braces
        
print("Tags in dogovor.docx:")
find_jinja_tags(docx_path)
