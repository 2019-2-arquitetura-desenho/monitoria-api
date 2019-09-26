# from django.test import TestCase
# from profiles.models import Student
# from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test.client import Client
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

class CheckProfilesAPITest(APITestCase):
    def setUp(self):
        self.user = create_new_user()

    # Test create Student, with all parameteres correct
    def test_create_student_sucess(self):
        token = self.user['token']
        response = create_student(token, 'Alfa Tester Beta', '123456789' , '4.99')
        self.assertEqual(response.status_code, HTTP_200_OK)

    # Test create Student, with wrong 'token'
    def test_create_student_wrong_token(self):
        response = create_student('1234thisisawrongtoken1234', 
                                'Alfa Tester Beta', 
                                '123456789' , 
                                '4.99')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
    
    # Test create Student, with invalid 'matricula' 
    def test_create_student_invalid_matricula(self):
        # not digits
        response = create_student(self.user['token'], 'Alfa Tester Beta', 'invalid', '4.99')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # insuficient digits
        response = create_student(self.user['token'], 'Alfa Tester Beta', '123', '4.99')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    # Test create Student, with invalid 'ira'  
    def test_create_student_invalid_ira_1(self):
        # ira should not be negative
        response = create_student(self.user['token'], 'Alfa Tester Beta', '123456789', '-1.0')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # ira should not be higher than 5.0
        response = create_student(self.user['token'], 'Welison Lucas Regis', '170024121', '6.0')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

     # Test create Student, with missing parameteres 
    def test_create_student_with_missing_parameteres(self):
        # without ira
        response = create_student(self.user['token'], 'Alfa Tester Beta', '123456789', None)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # without token
        response = create_student(None, 'Alfa Tester Beta', '123456789', '4.99')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # without name
        response = create_student(self.user['token'], None, '123456789', '4.99')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # without matatricula
        response = create_student(self.user['token'], None, '123456789', '4.99')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

def create_new_user():
    client = Client()
    data = {'email':'teste1@testando.com', 
            'password1': 'th1s1s4h4rdp455w0rd', 
            'password2': 'th1s1s4h4rdp455w0rd'}
    response = client.post('/registration/', data)
    return response.data

def create_student(token, name, matricula, ira):
    client = Client()
    data = {}
    if token:
        data['token'] = token
    if name:
        data['name'] = name
    if matricula:
        data['matricula'] = matricula
    if ira:
        data['ira'] = ira
    
    response = client.post('/create_profile/', data)
    return response