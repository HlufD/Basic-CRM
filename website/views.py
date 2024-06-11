from django.shortcuts import render,redirect
from  django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegistrationForm,AddRecordForm
from .models import Record
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"you have been logged in!")
            return redirect("home")
        else:
            messages.error(request,"Error happen while login")
            return redirect("home")
    else:
        records = Record.objects.all()
        return render(request,'home.html',{"records":records})

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out!")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
       form = RegistrationForm(request.POST)
       if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,"Registered successfully!")
            return redirect("home")
    else:
        form = RegistrationForm()
        return render(request,'register.html',{"form":form})
    
@login_required(login_url="home")
def customer_record(request,pk):
    record = Record.objects.get(id=pk)
    context = {"record":record}
    return render(request,'record.html',context)


@login_required(login_url="home")
def remove_record(request,pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,"Record Deleted successfully!")
    return redirect("home")


@login_required(login_url="home")
def add_record(request):
    form = AddRecordForm(request.POST)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Record Added!")
            return redirect("home")
    else:
        context={"form":form}
        return render(request,"add_record.html",context)
  
  
@login_required(login_url="home")   
def update_record(request,pk):
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None,instance=current_record)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Record updated!")
            return redirect("home")
    else:
        context ={"form":form}
        return render(request,'update_record.html',context)