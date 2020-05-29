from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import requests
import urllib, json, sys

# Create your views here.

#url = 'https://f3uvc5cpdd.execute-api.us-east-1.amazonaws.com/prod/authenticate'
headers = {'Content-type': 'application/json'}



def index(request):
    return render(request, 'demologin/index.html', {})

def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        #email = request.GET.get('email')
        #name = request.GET.get('name')
        #family_name = request.GET.get('family_name')
        url1="https://fnrryosh20.execute-api.us-east-1.amazonaws.com/Prod/login"
        response = requests.post(url1, json={'username': nickname, 'password': password}, headers=headers)
        print(nickname)
        print(password)
        #print('IMPRIMIR RESPONSE')
        #print(response.json())
        #print('Estado del codigo : ')
        #print(response.status_code)
        #print(response.json())
        json_data = json.dumps(response.json())
        data = json.loads(json_data)
        #print(data)
        #print(data['message'])
        if data['success'] == True:
            #response = response(headers={'Authorization': token},is_redirect=True,url="https://0q3wzpyww4.execute-api.us-east-1.amazonaws.com/prod/ping")
            token = data['data']['id_token']
            print('Imprimir Token desde success')    
            print(token)
            url_to = 'https://www.google.com'
            print(data['message'])
            #header = {'Authorization': '{}'.format(token)}
            #headers1 = {"Authorization": token}
            #print('Imprimir Header 2')
            #print(header)
            #response = redirect(url1)
            #response = {'Authorization': token}
            #response = redirect(url1) + response.headers
            #response = requests.post(url1, headers=header)
            #response = HttpResponseRedirect(url1)
            #response['Authorization'] = token
            #response.serialize_headers = {'Authorization': '{}'.format(token)}
            #print ('IMPRIMIR RESPONDSE ANTES DE RETURN')
            #print (response)
            #response.headers = { "Authorization": "Bearer " + token}
            #response = requests.get(url1,auth=headers1)
            #response = HttpResponseRedirect(url1)
            #response['TEST'] = 'TEST'
            #response = requests.post(url1,headers=header)
            #response = redirect(url1)
            #response.headers =  {'Authorization': '{}'.format(token)}
            #response = requests.request('POST',url1,headers=header)
            #r = requests.get(url1, headers={'Authorization': token})
            #print('IMPRIMIR RESPONSE DESPUES DE REDIRECT')
            #print(response.headers)
            #print(response)
            #request.redirect_to(url1)
            #response = requests.post(url1, headers=headers1)
            #context = { 'url' : 'https://0q3wzpyww4.execute-api.us-east-1.amazonaws.com/prod/ping',
            #    'Authorization' : token
            #}
            return HttpResponseRedirect(url_to)
        elif data['error'] == True:
            print(data['message'])
            return render(request, 'demologin/login.html', {})
    
    #if response.status_code == 200:
    #    redirect('demologin/home.html')

    return render(request, 'demologin/login.html', {})

def register(request):
    
    #print(nickname)
    #print(password)
    #print(email)
    #print(name)
    #print(family_name)
    #print(request.GET)
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        family_name = request.POST.get('family_name')
        url = 'https://fnrryosh20.execute-api.us-east-1.amazonaws.com/Prod/registrarse'
        response = requests.post(url, json={'username': nickname, 'password': password, 'name': name, 'email': email, 'family_name': family_name}, headers=headers)
        print(nickname)
        print(password)
        print(email)
        print(name)
        print(family_name)
        json_data = json.dumps(response.json())
        data = json.loads(json_data)
        #print(data)
        if data['error'] == True:
            msj = data['message']
            print(msj)    
        elif data['success'] == True:
            msj = data['message']
            print(msj)
    
    return render(request, 'demologin/register.html', {})

@login_required
def home(request):
    return render(request, 'demologin/home.html', {})