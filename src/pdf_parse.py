from pypdf import PdfReader

class Pdfs:

    def __init__(self, newpdf):
        self.pdf = PdfReader(newpdf)
        self.page_count = len(self.pdf.pages)
        self.pages = self.pdf.pages[:self.page_count]

    def get_all_text(self):
        text = ""

        for page in self.pages[:self.page_count]:
            text += " " + page.extract_text()

        return text

    def __get_single_page_text(self, page_index):
        text = ""

        text = self.pages[page_index].extract_text()

        return text