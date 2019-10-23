import pdftotext
import wget
import os
import re

class PdfExtractor:

    def __init__(self, reg_pdf):
        self.reg_pdf = reg_pdf

    def read_IRA(self):
        # creating regex
        pattern = '\d\.\d+'
        search = re.compile(pattern)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            IRA_extractor = pdftotext.PDF(f)
            ira = search.findall("\n\n".join(IRA_extractor))
            ira = ira[0]
            print()
            print(ira)

        return ira


if __name__ == "__main__":
    
    pdf_test = './tmp.pdf'
    obj = PdfExtractor(pdf_test)
    obj.read_IRA()
