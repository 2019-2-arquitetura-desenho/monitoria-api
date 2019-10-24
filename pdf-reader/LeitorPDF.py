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


class RegExtractor(Extractor):

    def extract(self):
        # creating regex
        pattern = r'(\d{2}/\d{7})'
        search = re.compile(pattern)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            reg_extractor = pdftotext.PDF(f)
            reg = search.findall("\n\n".join(reg_extractor))
            reg = reg[0]
            # print(reg)

        return reg


class SubExtractor(Extractor):

    def extract(self):
        # creating regex
        pattern1 = r'\d{6}  \w'
        pattern2 = r'\d{6}  \w.+'
        search = re.compile(pattern1)
        search2 = re.compile(pattern2)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            sub_extractor = pdftotext.PDF(f)

            # finding pattern1
            sub = search.findall("\n\n".join(sub_extractor))
            # finding subject codes
            sub_code = re.findall(r"\d{6}", "".join(sub))

            # finding pattern1
            sub2 = search2.findall("\n\n".join(sub_extractor))
            # finding subject grades
            sub_grade = re.findall(" [A-Z]{2} ", "".join(sub2))

            subs = [[sub_code[i], sub_grade[i]] for i in range(0, len(sub))]

            possible = [' MM ', ' MS ', ' SS ']

            sub_res = [i for i in subs if i[1] in possible]
            for i in sub_res:
                i[1] = i[1].replace(' ', '')
            sub_res = tuple(sub_res)
            # print(sub_res)

        return sub_res


def code(pdf_extractor: Extractor):
    pdf_extractor.extract()


if __name__ == "__main__":

    pdf_test = './tmp.pdf'
    code(IraExtractor(pdf_test))
    code(RegExtractor(pdf_test))
    code(SubExtractor(pdf_test))
