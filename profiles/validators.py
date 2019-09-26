def validate_digit(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a digit'),
            params={'value': value},
        )
        
def validate_matlen(value):
    if len(value)!=9:
        raise ValidationError(
            _('%(value)s has to be 9 digits'),
            params={'value': value},
        )