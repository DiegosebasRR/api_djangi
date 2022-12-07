from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import UsersSerializer
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404



from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_users': '/',
        'Search by Id': '/?user_id',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
  
    return Response(api_urls)

@api_view(['POST'])
def add_users(request):
    users = UsersSerializer(data=request.data)
  
    if Users.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if users.is_valid():
        users.save()
        return Response(users.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_users(request):
    if request.query_params:
        users = Users.objects.filter(**request.query_param.dict())
    else:
        users = Users.objects.all()
  
    if users:
        data = UsersSerializer(users)
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
def delete_users(request, pk):
    users = get_object_or_404(Users, pk=pk)
    users.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def update_users(request, pk):
    users = Users.objects.get(pk=pk)
    data = UsersSerializer(instance=users, data=request.data)
  
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_users(request):
    # checking for the parameters from the URL
    if request.query_params:
         users = Users.objects.filter(**request.query_param.dict())
         
    else:
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
    
    if users:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

class Login(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:view_users')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)

class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)
