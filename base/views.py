from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from base.models import  Profile


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            Profile.objects.create(user=user, role=role)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif profile.role == 'content_manager':
        return render(request, 'content_manager_dashboard.html')
    elif profile.role == 'student':
        return render(request, 'student_dashboard.html')
    else:
        return render(request, 'dashboard.html')


def student_signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            Profile.objects.create(user=user, role='student')
            return redirect('login')
        else:
            return render(request, 'student_signup.html', {'error': 'Passwords do not match'})
    return render(request, 'student_signup.html')

def question_view(request):
    return render(request, 'Questions.html')
