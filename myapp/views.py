from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm, UserDetailForm, CustomLoginForm
from .decorators import redirect_authenticated_user

# Create your views here.


def base(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        detail_form = UserDetailForm(request.POST, request.FILES)

        if user_form.is_valid() and detail_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            user_detail = detail_form.save(commit=False)
            user_detail.user = user
            user_detail.save()

            return redirect('login')  # or wherever you want to redirect after registration
    else:
        user_form = UserForm()
        detail_form = UserDetailForm()

    return render(request, 'register.html', {'user_form': user_form, 'detail_form': detail_form})


@redirect_authenticated_user
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page or home page
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')