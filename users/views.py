from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegister, UserUpdate, ProfileUpdate
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method =='POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for! you can login')
            return redirect('login')
    else:
        form = UserRegister()
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account Update')
            return redirect('profile')
    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)
