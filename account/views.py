from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd   = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'] )#checks for valid password and username
            if not(user is None):
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated Sucessfully')
                else:
                    return HttpResponse('Disable Account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form':form})

def register(request):
    if request.method == 'POST':
        user_form   = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # create new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the User Object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form':user_form})

#decorator to check user is acitve or not
@login_required
def edit(request):
    if request.method == 'POST':
        user_form    = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Edited Sucessfully')
            # return HttpResponse('test')
        else:
            messages.error(request, 'Error Updating the Profile')
    else:
        user_form       =  UserEditForm(instance=request.user)
        profile_form    =  ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', { 'user_form':user_form, 'profile_form':profile_form})




@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})
