import pdftotext
# import wget
# import os
import re
from abc import ABC, abstractmethod


class Extractor(ABC):

    def __init__(self, reg_pdf):
        self.reg_pdf = reg_pdf

    def template_method(self):
        self.extract()

    @abstractmethod
    def extract(self):
        pass


class IraExtractor(Extractor):

    def extract(self):
        # creating regex
        pattern = r'\d\.\d+'
        search = re.compile(pattern)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            IRA_extractor = pdftotext.PDF(f)
            ira = search.findall("\n\n".join(IRA_extractor))
            ira = ira[0]
            # print(ira)

        return ira


def code(pdf_extractor: Extractor):
    pdf_extractor.extract()


if __name__ == "__main__":

    pdf_test = './tmp.pdf'
    code(IraExtractor(pdf_test))
