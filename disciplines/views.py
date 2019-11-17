from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from disciplines.models import Class, Discipline, Period, ClassRegister, Meeting
from disciplines.serializers import ClassSerializer, DisciplineSerializer, PeriodSerializer, ClassRegisterSerializer, ClassRegisterShortSerializer
from rest_framework import viewsets
from django.utils import timezone
from monitoria.settings import SECRET_KEY, HEROKU_URL
import urllib
import json
import jwt
from django.test.client import Client
from profiles.models import Student, Profile, Professor, User
from datetime import date, datetime

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

@api_view(["POST"])
def get_discipline(request):
    pass

@api_view(["POST"])
def add_professor(request):
    pass

@api_view(["POST"])
def remove_professor(request):
    pass

@api_view(["POST"])
def create_period(request):
    initial_time = request.data.get('initial_time')
    end_time = request.data.get('end_time')

    if not initial_time or not end_time:
        return Response(data={'error': "Parametros obrigatorios: initial_time, end_time"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        initial_time = datetime.strptime(initial_time, '%Y-%m-%d').date()
        end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
    except:
        return Response(data={'error': "Parametros invalidos: initial_time, end_time"},
                        status=HTTP_400_BAD_REQUEST)

    if initial_time >= end_time:
        return Response(data={'error': "Periodo invalido (final <= inicio)"},
                        status=HTTP_400_BAD_REQUEST)

    conflict_periods = Period.objects.all()
    for period in conflict_periods:
        if  ((period.initial_time <= initial_time and period.end_time >= initial_time)
            or
            (period.initial_time >= initial_time and period.initial_time <= end_time)):
            return Response(data={'error': "Periodos nao podem existir simultaneamente"})

    # Colocar as disciplinas neste periodo
    try:
        response = urllib.request.urlopen(HEROKU_URL+'/discipline/?format=json')
        data = json.loads(response.read())
    except:
        return Response(data={'error': "Erro terminal: Erro durante a comunicação com o Crawler"},
                        status=HTTP_400_BAD_REQUEST)

    period = Period(initial_time=initial_time, end_time=end_time)
    period.save()
    for discipline in data:
        try:
            temp_discipline = Discipline.objects.get(code=discipline['code'])
        except Discipline.DoesNotExist:
            temp_discipline = Discipline()
        temp_discipline.name = discipline['name']
        temp_discipline.code = discipline['code']
        temp_discipline.save()
        for each in discipline['discipline_class']:
            temp_class = Class()
            temp_class.name = each['name']
            temp_class.vacancies = each['vacancies']
            temp_class.shift = each['shift']
            temp_class.professors = []
            for professor in each['teachers']:
                temp_class.professors.append(professor['name'])
            meetings_list = []
            for meet in each['meetings']:
                try:
                    meeting = Meeting.objects.get(
                        day=meet['day'], init_hour=meet['init_hour'], 
                        final_hour=meet['final_hour'], room=meet['room']
                    )
                    meeting.save()
                except Meeting.DoesNotExist:
                    meeting = Meeting.objects.create(
                        day=meet['day'], init_hour=meet['init_hour'], 
                        final_hour=meet['final_hour'], room=meet['room']
                    )
                    meeting.save()
                meetings_list.append(meeting)
            temp_class.discipline = temp_discipline
            temp_class.period = period
            temp_class.save()
            temp_class.meetings.set(meetings_list)
            temp_class.save()
    
    serializer = PeriodSerializer(period)
    return Response(data=serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def register_discipline(request):
    jwt_token = request.data.get('token')
    discipline_code = request.data.get('discipline_code')
    class_name = request.data.get('class_name')
    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    
    try:
        user = User.objects.get(pk=user_obj['user_id'])
        profile = Profile.objects.get(user=user)
        student = Student.objects.get(profile=profile)
    except (Student.DoesNotExist, Profile.DoesNotExist, User.DoesNotExist):
        return Response(data={'error': "Erro terminal: Falha ao localizar perfil"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        time_now = timezone.now().date()
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
    except Period.DoesNotExist:
        return Response(data={'error': "Fora do período de inscrição"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        discipline = Discipline.objects.get(code=discipline_code)
    except:
        return Response(data={'error': "Erro terminal: Falha ao localizar disciplina"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        temp_class = Class.objects.filter(discipline=discipline, period=period).get(name=class_name)
    except:
        return Response(data={'error': "Erro terminal: Falha ao localizar turmas"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        class_register = ClassRegister.objects.filter(discipline_class=temp_class).get(student=student)
        return Response(data={'error': "Estudante ja esta cadastrado na turma"},
                        status=HTTP_400_BAD_REQUEST)
    except ClassRegister.DoesNotExist:
        class_register = ClassRegister(student=student, discipline_class=temp_class)
        try:
            calculate_points(class_register)
        except RegisterException:
            return Response(data={'error': "Estudante não cursou a materia"},
                            status=HTTP_400_BAD_REQUEST)
        class_register.save()
        serializer = ClassRegisterSerializer(class_register)
        return Response(data=serializer.data, status=HTTP_200_OK)


class RegisterException(Exception):
    pass
def calculate_points(class_register):
    values = {
        "SS": 5.0,
        "MS": 4.0,
        "MM": 3.0,
    }
    for each in class_register.student.academic_record:
        if each[0]==str(class_register.discipline_class.discipline.code):
            if class_register.indication==None:
                class_register.points = (values[each[1]]*0.6) + (class_register.student.ira*0.4)
            else:
                class_register.points = (values[each[1]]*0.3) + (class_register.student.ira*0.2)+(class_register.indication*0.5)
            class_register.save()
            return 
    raise RegisterException("Estudante não cadastrado na disciplina")

@api_view(["POST"])
def get_class_ranking(request):
    discipline_code = request.data.get('discipline_code')
    class_name = request.data.get('class_name')

    if not discipline_code or not class_name:
        return Response(data={'error': "Parametros obrigatorios: discipline_code, class_name"})

    discipline = Discipline.objects.get(code=discipline_code)

    try:
        time_now = timezone.now().date()
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
    except Period.DoesNotExist:
        return Response(data={'error': "Fora do período de inscrição"},
                        status=HTTP_400_BAD_REQUEST)

    discipline_class = Class.objects.get(discipline=discipline, name=class_name, period=period)

    ranking = []
    registrations = ClassRegister.objects.filter(discipline_class=discipline_class)

    discipline_name = discipline.name
    for register in registrations:
        temp_name = register.student.profile.name
        temp_matricula = register.student.matricula
        temp_points = register.points
        ranking.append([temp_points, temp_matricula, temp_name])

    sorted(ranking)
    for each in ranking:
        each[0], each[2] = each[2], each[0]

    data = {'materia': discipline_name,
            'ranking': ranking}

    return Response(data=data, status=HTTP_200_OK)

@api_view(["POST"])
def get_student_rankings(request):
    jwt_token = request.data.get('token')

    # Validação do token
    client = Client()
    response = client.post('/token_verify/', request.data)
    if response.status_code != HTTP_200_OK:
        return response
    # Decodificação do usuário
    user_obj = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])

    try:
        time_now = timezone.now().date()
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
    except Period.DoesNotExist:
        return Response(data={'error': "Fora do período de inscrição"},
                        status=HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_obj['user_id'])
        profile = Profile.objects.get(user=user)
        student = Student.objects.get(profile=profile)
        registers = ClassRegister.objects.filter(student=student)
    except (Student.DoesNotExist, User.DoesNotExist, Profile.DoesNotExist):
        return Response(data={'error': "Erro terminal: Falha ao localizar perfil"},
                        status=HTTP_400_BAD_REQUEST)

    data = {'data': []}
    client = Client()
    for register in registers:
        if register.discipline_class.period != period:
            continue
        body = {'discipline_code': register.discipline_class.discipline.code,
                'class_name': register.discipline_class.name}
        response = client.post('/get_class_ranking/', body)
        data['data'].append(response.data)

    return Response(data=data, status=HTTP_200_OK)
@api_view(["GET"])
def get_winners(request):
    # Vagas por disciplina
    classes = Class.objects.all()
    vacancies = {}
    for eatch in classes:
        vacancies[eatch.id] = int(eatch.vacancies*0.1) # Vagas para monitor 10%

    # Estudantes escolhidos
    students = Student.objects.all()
    print('students', students)
    chose_student = {}
    for eatch in students:
        chose_student[eatch.matricula] = False

    
    data = ClassRegister.objects.order_by('priority', '-points')
    registers = []
    for eatch in data:
        registers.append(eatch)
    print('registers', registers)
    i = 0
    ans = []
    while registers:
        print('Start over qrst', len(registers))
        if i>=len(registers):
            break
        register = registers[i]
        student_id = register.student.matricula
        class_id = register.discipline_class.id
        if chose_student[student_id]:
            print('Student alredy chosen ', student_id)
            registers.pop(i)
            i = 0
        elif vacancies[class_id]:
            print('Student chosen ', student_id)
            res = ClassRegister.objects.get(student=register.student)
            ans.append(res)
            vacancies[class_id]-=1
            chose_student[student_id]=True
            registers.pop(i)
            i = 0
        else:
            i+=1
    #print('ans', ans)
    serializer = ClassRegisterShortSerializer(ans, many=True)
    return Response(data=serializer.data, status=HTTP_200_OK)
