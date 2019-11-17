from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from disciplines.models import Period
from django.utils import timezone


def get_current_period():
    try:
        time_now = timezone.now().date()
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
        return Response(status=HTTP_200_OK), period

    except Period.DoesNotExist:
        return Response(data={'error': "Fora do período de inscrição"},
                        status=HTTP_400_BAD_REQUEST), None

def get_closest_period():
    try:
        periods = Period.objects.filter(end_time__gte=time_now)
        period = periods.get(initial_time__lte=time_now)
    except Period.DoesNotExist:
        try:
            period = Period.objects.order_by('-end_time').get()
        except Period.DoesNotExist:
            return Response(data={'error': "Nenhum processo de monitoria encontrado"},
                            status=HTTP_400_BAD_REQUEST)
    return Response(status=HTTP_200_OK), period