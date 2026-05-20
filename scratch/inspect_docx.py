import docx
import os

doc_path = r'c:\Users\User\dev\docs_create\main\document_templates\dogovor.docx'
if os.path.exists(doc_path):
    doc = docx.Document(doc_path)
    for i, table in enumerate(doc.tables):
        print(f"Table {i}:")
        for r, row in enumerate(table.rows):
            cells = [cell.text for cell in row.cells]
            print(f"  Row {r}: {cells}")
else:
    print("File not found")
