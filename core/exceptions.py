from rest_framework.exceptions import APIException
from django.utils.translation import ugettext as _


class InvalidPassword(APIException):
    status_code = 404
    default_detail = 'Senha inválida'
    default_code = 'permission_denied'


class ForgotPasswordInvalidParams(APIException):
    status_code = 404
    default_detail = _('Parametros inválidos')
    default_code = 'permission_denied'


class ForgotPasswordExpired(APIException):
    status_code = 404
    default_detail = _('Link expirado')
    default_code = 'permission_denied'
