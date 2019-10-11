# from django.test import TestCase
# from profiles.models import Student
# from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test.client import Client
from rest_framework.status import *


class CheckProfilesAPITest(APITestCase):
    # Test create Student with all parameteres correct
    def test_create_profile_success(self):
        response = create_profile(email='teste2@testando.com', password='th1s1s4h4rdp455w0rd', name='Alpha Test')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    # Test create Student with wrong 'token'
    def test_create_profile_wrong_email(self):
        response = create_profile(email='teste2.', password='th1s1s4h4rdp455w0rd', name='Alpha Test')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

     # Test create Student with missing parameteres 
    def test_create_profile_with_missing_parameteres(self):
        # without email
        response = create_profile(password='th1s1s4h4rdp455w0rd', name='Alpha Test')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # without password
        response = create_profile(email='teste3@testando.com', name='Alpha Test')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        # without name
        response = create_profile(email='teste3@testando.com', password='th1s1s4h4rdp455w0rd')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    # Test edit Student with all parameteres correct
    def test_edit_profile_success(self):
        new_name = 'Alfa Other Name'
        response = create_profile(email='teste4@testando.com', password='th1s1s4h4rdp455w0rd')
        jwt_token = response.data['token']
        response = edit_profile(token=jwt_token, name=new_name)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], new_name)

    # Test edit Student with invalid 'token'
    def test_edit_profile_invalid_token(self):
        response = edit_profile(token='invalid_token')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
    #Test get_profile
    def test_get_profile_success(self):
        response = create_profile(email='teste5@testando.com', password='th1s1s4h4rdp455w0rd')
        jwt_token = response.data['token']
        profile = response.data['profile']
        response = get_profile(token=jwt_token)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, profile)

def create_profile(email='', password='', name=''):
    client = Client()
    data = {
        'email':email,
        'password':password,
        'name':name
    }
    response = client.post('/registration/', data)
    return response

def edit_profile(token='', name=''):
    client = Client()
    data = {
        'token':token,
        'name':name
    }
    response = client.post('/set_profile/', data)
    return response
def get_profile(token=''):
    client = Client()
    data = {'token':token}
    response = client.post('/get_profile/', data)
    return response