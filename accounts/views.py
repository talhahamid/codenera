from django.shortcuts import render,redirect
from accounts.models import Users
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import FileSystemStorage



def register(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        
        if confirm_password==password:
            if Users.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('/register/')
            elif Users.objects.filter(mobile=mobile).exists():
                messages.info(request,'Mobile exists')
                return redirect('/register/')
            else:
                password=make_password(password)
                user=Users.objects.create(name=name,email=email,mobile=mobile,password=password)
                user.save()
                return redirect('/')  
        else:  
            messages.info(request,'Password and Confirm Password doesnt match')
            return redirect('/accounts/register/')
    return render(request,'register.html')




def login(request):
    if request.method=="POST":
        mobile=request.POST['mobile']
        password=request.POST['password']
        try:
            user=Users.objects.get(mobile=mobile)
            if user.mobile==int(mobile) and check_password(password,user.password):
                request.session['id']=user.id
                return redirect('/convert/home/')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('/')            
        except ObjectDoesNotExist:
            messages.info(request,'Mobile doesnot exists')
            return redirect('/')    
    return render(request,'login.html')




def logout(request):
    request.session.flush()
    return redirect('/')