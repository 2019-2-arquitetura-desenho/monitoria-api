import pdftotext
import wget
# import os
import re
from abc import ABC, abstractmethod
import json
import requests


class Extractor(ABC):

    def __init__(self, reg_pdf):
        self.reg_pdf = reg_pdf

    def template_method(self):
        ira = self.extractIra()
        reg = self.extractReg()
        sub = self.extractSub()

        return ira, reg, sub

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
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            IRA_extractor = pdftotext.PDF(f)
            try:
                ira = search.findall("\n\n".join(IRA_extractor))
                ira = ira[0]
                # print()
                # print(ira)
            except Exception:
                return False

        return ira

    def extractReg(self):
        # creating regex
        pattern = r'(\d{2}/\d{7})'
        search = re.compile(pattern)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            reg_extractor = pdftotext.PDF(f)
            try:
                reg = search.findall("\n\n".join(reg_extractor))
                reg = reg[0]
            except Exception:
                return False
            # print(reg)

        return reg

    def extractSub(self):
        # creating regex
        pattern1 = r'\d{6}  \w'
        pattern2 = r'\d{6}  \w.+'
        search = re.compile(pattern1)
        search2 = re.compile(pattern2)
        # opening pdf file
        with open(self.reg_pdf, 'rb') as f:
            sub_extractor = pdftotext.PDF(f)

            try:
                # finding pattern1
                sub = search.findall("\n\n".join(sub_extractor))
                # finding subject codes
                sub_code = re.findall(r"\d{6}", "".join(sub))

                # finding pattern1
                sub2 = search2.findall("\n\n".join(sub_extractor))
                # finding subject grades
                sub_grade = re.findall(" [A-Z]{2} ", "".join(sub2))

                subs = [[sub_code[i], sub_grade[i]]
                        for i in range(0, len(sub))]

                possible = [' MM ', ' MS ', ' SS ']

                sub_res = [i for i in subs if i[1] in possible]
                for i in sub_res:
                    i[1] = i[1].replace(' ', '')
                sub_res = tuple(sub_res)
                # print(sub_res)

            except Exception:
                return False

        return sub_res


def extract_code(pdf_extractor: Extractor):
    ira, reg, sub = pdf_extractor.template_method()

    if not ira or not reg or not sub:
        error_json = {
            'Error': 'PDF Invalido'
        }

        # print(error_json)
        return error_json

    student_info = {
        'matricula': reg,
        'ira': ira,
        'materias': sub
    }

    # student_info['Matricula'] = reg
    # student_info['Materias'] = sub
    # student_info['IRA'] = ira

    json_data = json.dumps(student_info)
    # print(json_data)
    return json_data


class Download():
    def PDFdownload(url):
        wget.download(url, './tmp.pdf')
        local = './tmp.pdf'
        return local

    def XMLdownload(url):
        wget.download(url, './tmp.xml')
        local = './tmp.xml'
        return local


def getUrl():
    response = requests.get('http://localhost:8000/get_student')
    url = response.json()['pdf_url']
    # url = 'https://res.cloudinary.com/gustavolima00/image/upload/v1571400279/historico.pdf'
    pdf_test = Download.PDFdownload(url)
    return pdf_test

if __name__ == "__main__":
    print(extract_code(PDFExtractor(getUrl())))
