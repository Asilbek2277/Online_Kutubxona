from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from .models import *

def bolimlar(request):
    context={
        'bolim': Bolim.objects.all()
    }
    return render(request, 'Bolimlar.html', context)



class KitoblarView(View):
    def get(self, request):
            context={
                'kitob': Kitob.objects.order_by('nomi'),
                'muallif': Muallif.objects.all(),
                'bolim': Bolim.objects.all()
            }
            return render(request, 'kitoblar.html', context)
    def post(self, request):
        if request.user.is_authenticated:
            Kitob.objects.create(
                user=request.user,
                nomi=request.POST['nomi'],
                muallif=Muallif.objects.get(id=request.POST['muallif']),
                yili=request.POST['yili'],
                bolim=Bolim.objects.get(id=request.POST['bolim']),
                file=request.POST['file']
            )
            return redirect('/kitoblar/')

class KitobView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            context={
                "kitob": Kitob.objects.get(id=pk)
            }
            return render(request, 'kitob.html', context)



class KitoblarimView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context={
                'kitoblarim': Kitob.objects.filter(user=request.user)
            }
            return render(request, 'kitoblarim.html', context)



def tahrirlash(request, pk):
    if request.user.is_authenticated:
        if request.method=='POST':
            kitob=Kitob.objects.get(id=pk)
            if kitob.user==request.user:
                kitob.nomi=request.POST['nomi']
                kitob.muallif=Muallif.objects.get(id=request.POST['muallif'])
                kitob.yili=request.POST['yili']
                kitob.bolim=Bolim.objects.get(id=request.POST['bolim'])
                kitob.file=request.POST['file']
                kitob.save()

                return redirect('/kitoblar/')
            return redirect('/')

        context={

            'kitob': Kitob.objects.get(id=pk),
            'muallif': Muallif.objects.all(),
            'bolim': Bolim.objects.all()

        }

        return render(request, 'tahrirlash.html', context)
    return redirect('/')



def ochirish(request, pk):
    if request.user.is_authenticated:
        if Kitob.objects.get(id=pk).user == request.user:
            Kitob.objects.get(id=pk).delete()
            return redirect('/kitoblar/')
    return redirect('/')



def yangi(request):
    context={
        'kitob': Kitob.objects.filter(muallif__tirik=True)
    }
    return render(request, 'yangi.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user= authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('/kitoblar/')
        return redirect('/')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')