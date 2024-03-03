# permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsGetMethodOrIsAdmin(BasePermission):
    """ Classe customizada que permite requisições GET sem autenticação"""
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin
