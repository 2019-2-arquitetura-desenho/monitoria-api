import pdftotext
import wget
# import os
import re
from abc import ABC, abstractmethod


class Extractor(ABC):

    def __init__(self, reg_pdf):
        self.reg_pdf = reg_pdf

    def template_method(self):
        self.extractIra()
        self.extractReg()
        self.extractSub()

    @abstractmethod
    def extractIra(self):
        pass

    @abstractmethod
    def extractReg(self):
        pass

    @abstractmethod
    def extractSub(self):
        pass

class PDFExtractor(Extractor):
    def extractIra(self):
        # creating regex
        pattern = r'\d\.\d+'
        search = re.compile(pattern)

    def extractReg(self):
        # creating regex
        pattern = r'(\d{2}/\d{7})'
        search = re.compile(pattern)

    def extractSub(self):
        # creating regex
        pattern1 = r'\d{6}  \w'
        pattern2 = r'\d{6}  \w.+'
        search = re.compile(pattern1)
        search2 = re.compile(pattern2)

def extract_code(pdf_extractor: Extractor):
    pdf_extractor.template_method()


class Download():
    def PDFdownload(self):
        wget.download(url, './tmp.pdf')
        local = './tmp.pdf'
        return local

    def XMLdownload(self):
        wget.download(url, './tmp.xml')
        local = './tmp.xml'
        return local


if __name__ == "__main__":
    url = 'https://res.cloudinary.com/gustavolima00/image/upload' + '/v1571400279/historico.pdf'
    pdf_test = Download.PDFdownload(url)
    extract_code(PDFExtractor(pdf_test))
