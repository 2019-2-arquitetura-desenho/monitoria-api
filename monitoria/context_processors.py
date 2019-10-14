from django.conf import settings


def global_settings(request):
    # return any necessary values
    # return {
    #     'THING1': settings.VAR1,
    #     'THING2': settings.VAR2
    # }
    return {'DOMAIN': settings.DOMAIN}
