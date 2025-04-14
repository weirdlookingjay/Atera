from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

@method_decorator(ensure_csrf_cookie, name='dispatch')
class AccountViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'])
    def get_csrf_token(self, request):
        return Response({"detail": "CSRF cookie set"})
