from django.shortcuts import render,redirect,HttpResponse
from smsapp.emailBackend import emailBackend
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from smsapp.models import CustomUser


def BASE (request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        user = emailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request, 'Email and Password are invalid!')
                return redirect('login')
        else:
            messages.error(request, 'Email and Password are invalid!')
            return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id )

    context = {
        "user":user,
    }

    return render(request, 'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic

            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, 'Your Profile Has Been Updated Successfully')
            return redirect('profile')
        except:
            messages.error(request, 'Profile update failed. Please try again.')

    return render(request, 'profile.html')