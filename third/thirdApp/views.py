from django.shortcuts import render
from django import forms

from thirdApp.models import UserProfileInfo
from thirdApp.forms import UserProfileInfoForm,UserForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def homepage(request):
    my_dict = {'one':'hello','two':100}
    return render(request,"thirdApp/index.html",context=my_dict)

def page_1(request):
    return render(request,"thirdApp/other.html")

def page_2(request):
    return render(request,"thirdApp/relative_url_template.html")

@login_required
def user_logout(request):
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def special(request):
    HttpResponse("You are logged in !")

def form_page(request):

    registered = False

    # CHECK IF WE GET A POST BACK
    if request.method == 'POST':
        # IN WHICH CASE WE PASS IN THAT REQUEST
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        #CHECK IF FORM IS VALID
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,"thirdApp/registrate.html",
        {'form_user':user_form,
        'form_profile':profile_form,
        'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('homepage'))
            else:
                return HttpResponse("Your account is not active")
        else:
            print("Someone tried log in with username {} and password {}".format(username,password))
            return HttpResponse("Invalid login details")
    else:
        return render(request,"thirdApp/login.html")
