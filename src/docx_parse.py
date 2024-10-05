from docx import Document

class Docs:

    def __init__(self, newdocument):
        self.document = Document(newdocument)

    # prints all paragraphs
    def get_paragraphs(self):
        text = ""

        for paragraph in self.document.paragraphs:
            text += paragraph.text

        print(f"{paragraph.text}")
        #return text

    # prints all tables
    def get_tables(self):
        tables = ""

        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        tables += " " + para.text

        print(tables)
        #return tables

    # # prints images information
    # def get_images(self):
    #     for image in self.document.inline_shapes:
    #         print(f"{image}")

    def get_headings(self):
        for content in self.document.paragraphs:
            if content.style.name=='Heading 1':
                print(f"{content.text}")

doc = Docs("D:\\Full Sail Master\\csms_summarize\\csms_summarize\\src\\test_files\\worddocexample.docx")
doc.get_tables()