from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from disciplines.models import Class, Discipline, Period, ClassRegister, Meeting
from disciplines.serializers import (
    ClassSerializer, 
    DisciplineSerializer, 
    PeriodSerializer, 
    ClassRegisterSerializer, 
    ClassRegisterShortSerializer,
    MeetingSerializer
)
from rest_framework import viewsets
from django.utils import timezone
from monitoria.settings import SECRET_KEY, HEROKU_URL
import urllib
import json
import jwt
from django.test.client import Client
from profiles.models import Student, Profile, Professor, User
from datetime import date, datetime
from profiles.helpers import get_user, get_profile
from disciplines.helpers import get_current_period, get_closest_period

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

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
    priority = request.data.get('priority')
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
        # return Response(data={'error': "Estudante ja esta cadastrado na turma"},
        #                 status=HTTP_400_BAD_REQUEST)
    except ClassRegister.DoesNotExist:
        class_register = ClassRegister(student=student, discipline_class=temp_class)
    if priority:
        class_register.priority = priority
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
    class_register.save()
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
def get_rankings(request):
    jwt_token = request.data.get('token')

    #Getting student/teacher
    response, student = get_profile(jwt_token)
    if response.status_code!=HTTP_200_OK:
        return response

    #Getting period
    response, period = get_current_period()
    if response.status_code!=HTTP_200_OK:
        response, period = get_closest_period()
        if response.status_code!=HTTP_200_OK:
            return response
        calculate_period(period)

    data = []
    classes = Class.objects.filter(period=period)
    if student.profile.is_professor:
        professor = student
        list_classes = []
        for each in classes:
            if professor.profile.name in each.professors and not each in list_classes:
                list_classes.append(each)
        for discipline_class in list_classes:
            ranking = ClassRegister.objects.filter(discipline_class=discipline_class).order_by('-points')
            ranking = ClassRegisterSerializer(ranking, many=True).data
            discipline = discipline_class.discipline 
            discipline_data = {}
            discipline_data['discipline'] = discipline.name
            discipline_data['class'] = discipline_class.name
            discipline_data['vacancies'] = int(discipline_class.vacancies*0.1)
            discipline_data['ranking'] = ranking
            data.append(discipline_data)

    else:
        registers = ClassRegister.objects.filter(discipline_class__in=classes, student=student)
        for register in registers:
            ranking = ClassRegister.objects.filter(discipline_class=register.discipline_class).order_by('-points')
            ranking = ClassRegisterSerializer(ranking, many=True).data
            discipline = register.discipline_class.discipline 
            discipline_data = {}
            discipline_data['discipline'] = discipline.name
            discipline_data['class'] = register.discipline_class.name
            discipline_data['vacancies'] = int(register.discipline_class.vacancies*0.1)
            discipline_data['ranking'] = ranking
            data.append(discipline_data)

    return Response(data=data, status=HTTP_200_OK)

@api_view(["POST"])
def indicate_student(request):
    jwt_token = request.data.get('token')
    register_id = request.data.get('register_id')
    points = request.data.get('points')

    points_error = Response(data={'error': "Points deve ser um inteiro entre 1 e 5"},
                        status=HTTP_400_BAD_REQUEST)
    

    try:
        points = float(points)
        if points<1 or points>5:
            return points_error
    except ValueError:
        return points_error
    try:
        register_id = int(register_id)
        register = ClassRegister.objects.get(id=register_id)
    except (ValueError, ClassRegister.DoesNotExist):
        return Response(data={'error': "Registro não existe"},
                        status=HTTP_400_BAD_REQUEST)
    response, professor = get_profile(jwt_token)
    if response.status_code!=HTTP_200_OK:
        return response
    if not professor.profile.is_professor:
        return Response(data={'error': "Erro terminal: Falha ao localizar professor no sistema"},
                        status=HTTP_400_BAD_REQUEST)

    if not professor.profile.name in register.discipline_class.professors:
        return Response(data={'error': "Professor foi não localizado nesta classe"},
                        status=HTTP_400_BAD_REQUEST)
    register.indication = points
    calculate_points(register)
    register.save()
    serializer = ClassRegisterSerializer(register)
    return Response(data=serializer.data, status=HTTP_200_OK)

def calculate_period(period):
    if period.calculated:
        return
    client = Client()
    response = client.post('/calculate_winners/', {'date':period.initial_time})
    if response.status_code==HTTP_200_OK:
        period.calculated = True
        period.save()
    return 

@api_view(["POST"])
def calculate_winners(request):
    # Vagas por disciplina
    time_now = request.data.get('date')
    try:
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
    except Period.DoesNotExist:
        return Response(data={'error': "Falha ao localizar periodo de monitoria"},
                        status=HTTP_400_BAD_REQUEST)
    
    classes = Class.objects.filter(period=period)
    vacancies = {}
    for eatch in classes:
        vacancies[eatch.id] = int(eatch.vacancies*0.1) # Vagas para monitor 10%
    # Estudantes escolhidos
    students = Student.objects.all()
    chose_student = {}
    for eatch in students:
        chose_student[eatch.matricula] = False

    data = ClassRegister.objects.filter(discipline_class__in=classes)
    data = data.order_by('priority', '-points')
    registers = []
    for eatch in data:
        registers.append(eatch)
    print('registers', registers)
    i = 0
    ans = []
    while registers:
        if i>=len(registers):
            break
        # Student ja inscrito em uma monitoria
        register = registers[i]
        student_id = register.student.matricula
        if chose_student[student_id]:
            print('Student alredy chosen ', student_id)
            register.status = 'Reprovado'
            register.save()
            registers.pop(i)
            i = 0
            continue
        
        # Get student position
        ranking = ClassRegister.objects.filter(discipline_class=register.discipline_class).order_by('-points')
        position = 1
        for eatch in ranking:
            if eatch==register:
                break
            position+=1
  
        # Student está dentro das vagas
        class_id = register.discipline_class.id
        if vacancies[class_id]>=position:
            print('Student chosen ', student_id)
            register.status = 'Aprovado'
            register.save()
            ans.append(register)
            vacancies[class_id]-=1
            chose_student[student_id]=True
            registers.pop(i)
            i = 0
            continue
        else:
            # Estudante não está dentro das vagas, mas pode ficar
            i+=1
            continue

    # Cadastros não contemplados
    for register in registers:
        register.status = 'Reprovado'
        register.save()
    serializer = ClassRegisterShortSerializer(ans, many=True)
    return Response(data=serializer.data, status=HTTP_200_OK)
