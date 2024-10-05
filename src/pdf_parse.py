from pypdf import PdfReader

class Pdfs:

    def __init__(self, newpdf):
        self.pdf = PdfReader(newpdf)
        self.page_count = len(self.pdf.pages)
        self.pages = self.pdf.pages[:self.page_count]

    # prints all text
    def get_all_text(self):
        text = ""

        for page in self.pages[:self.page_count]:
            text += page.extract_text()

        print(f"{text}")
        #return text

    def get_single_page_text(self, page_index):
        text = ""

        text = self.pages[page_index].extract_text()

        print(f"{text}")
        #return text
        

pdf = Pdfs("D:\\Full Sail Master\\Ortiz_Capstone_Pitch_Ideas.pdf")
pdf.get_all_text()