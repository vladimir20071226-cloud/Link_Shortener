from django.shortcuts import render, redirect, get_object_or_404
from .models import Link, ShortUrl
from .decode_and_encode_hex import encode_hex, decode_hex
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, timezone
import requests
def index(request):
    return render(request, "index.html")


def create_short_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        if not original_url:
            return render(request, "error.html", {"message": "Не указан URL"})
        link = Link.objects.create(original_url=original_url)
        short_code = reverse('redirect_url', args=[link.id])
        return render(request, 'shortened.html', {'short_code': short_code})

#def shorten_url(request):
#    if request.method == 'POST':
#        original_url = request.POST.get("url")
#       if not original_url:
#           return render(request, "error.html", {"message": "Не указан URL"})
#        url = Link.objects.create(original_url=original_url)
#        short_code = encode_hex(url.id)
#        return JsonResponse({"short_url": f"http://127.0.0.1:8000/{short_code}"})
#    return render(request, "error.html", {"message": "Метод запроса не поддерживается"})

def redirect_url(request, pk):
    try:
        url = Link.objects.get(pk=pk)
        url.click_count += 1
        url.save()
    except ValueError:
        return render(request, "error.html", {"message": "Неверный код ссылки"})
    except ObjectDoesNotExist:
        return render(request, "error.html", {"message": "Ссылка не найдена"})
    return redirect(url.original_url)


def user_login(request):
    if request.method == 'POST':
        password=request.POST['password']
        username=request.POST['username']
        user=authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return render(request, 'login_success.html')
        else:
            return render(request, 'login_failed.html', {'username': username})
    return render(request, 'login.html')
def stats(request, pk):
    url_obj=get_object_or_404(Link, pk=pk)
    return render(request, 'stats.html', {'url': url_obj,
                                          'delete_url': reverse('link_delete', args=[url_obj.pk]),
                                          'copy_url': reverse('link_copy', args=[url_obj.pk])})
@csrf_exempt
def link_delete(request, pk):
    if request.method=='POST':
        link=Link.objects.get(pk=pk)
        link.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'status': 400})
def link_copy(request, pk):
    link=get_object_or_404(Link, pk=pk, user=request.user)
    new_link=Link.objects.create(original_url=link.original_url,
                                 user=request.user)
    new_link.code=encode_hex(new_link.pk)
    new_link.save()
    return redirect('stats', code=new_link.code)
def recent_links(request):
    week_ago=timezone.now()-timedelta(weeks=1)
    links = ShortUrl.objects.filter(updated_at__gte=week_ago, link__user=request.user)
    return render(request,'recent_links.html', {'links': links})

def user_logout(request):
    logout(request)
    return redirect('index')
def user_register(request):
    if request.method == 'POST':
        password=request.POST.get('password')
        username=request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Имя уже занято'})
        user=User.objects.create_user(username=username, password=password)
        login(request, user)
        return  redirect('index')
    return render(request, 'register.html')
def login_google(request):
    url = ("https://accounts.google.com/o/oauth2/auth"
        "?client_id=646850686903-ovuh53047frn24ioe5icorcdd6sjcog8"
        "&redirect_uri=http://localhost:8000/auth/google/callback"
        "&response_type=code"
        "&scope=openid email profile")
    return redirect(url)
    
def google_callback(request):
    code=request.GET.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {"code": code,
            "client_id": "646850686903-ovuh53047frn24ioe5icorcdd6sjcog8",
            "client_secret": "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",
           "redirect_uri": "http://localhost:8000/auth/google/callback",
           "grant_type": "authorization_code"}
    token_response=requests.post(token_url, data=data)
    tokens=token_response.json()
    access_token=tokens.get("access_token")
    user_info=requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers= {"Authorization": f"Bearer {access_token}"}).json()
    return render (request,'login_success.html', {'user_info': user_info})



