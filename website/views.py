from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm

class Homepage(View):

    def get(self, request):
        return render(request,template_name='homepage.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print (username)
        print (password)
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfull")
            return redirect('homepage')
        else:
            messages.success(request, "Error occured, please try again!")
            return redirect('homepage')
    

class Logout_user(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfull")
        return redirect('homepage')
    
class Register_User(View):
    def get(self, request):
        form = SignUpForm()
        return render(request,template_name='register.html', context={'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('homepage')
        else:
            messages.success(request, "Error occured, Please try again!")
            return redirect('register')
