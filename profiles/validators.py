from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_ira(value):
    try:
        value=float(value)
    except:
        raise ValidationError(
            _('%(value)s is not a float'),
            params={'value': value},
        )
    if value<0.0 or value>5.0:
        raise ValidationError(
            _('%(value)s is not a between 0 and 5'),
            params={'value': value},
        )
    
        
def validate_mat(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a digit'),
            params={'value': value},
        )
    if len(value)!=9:
        raise ValidationError(
            _('%(value)s has to be 9 digits'),
            params={'value': value},
        )