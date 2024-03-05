from django.core.exceptions import ValidationError

def IsPositive(value):
    if value < 0:
        raise ValidationError('Valor deve ser positivo')