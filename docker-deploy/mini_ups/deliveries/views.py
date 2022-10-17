import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse
from .models import *

# Create your views here.
from .forms import UserSignUpForm, PackageForm, AdminPackageForm, UPSAccountForm


def home(request):
    return render(request, "home.html", {})


# def track_package(request, package_id):
#     package_id =
#

def package_view(request):
    # tracking_number == package_id
    tracking_number = request.GET.get("q")
    try:
        selected_package = Package.objects.get(package_id=tracking_number)
    except Package.DoesNotExist:
        selected_package = None
    context = {'selected_package': selected_package}
    return render(request, "package_detail.html", context)

def package_view_with_id(request, tracking_number):
    # tracking_number == package_id
    try:
        selected_package = Package.objects.get(package_id=tracking_number)
    except Package.DoesNotExist:
        selected_package = None
    context = {'selected_package': selected_package}
    return render(request, "package_detail.html", context)


def account_package_tracking(request):
    # ups_account = models.ForeignKey(UPSAccount, null=True, on_delete=models.CASCADE)
    packages = Package.objects.filter(ups_account__user_id=request.user.id)
    ups_account = UPSAccount.objects.get(user_id=request.user.id)
    # context = {'packages': packages}
    context = {'packages': packages, 'ups_account': ups_account}
    return render(request, "account_package_tracking.html", context)

def package_create(request):
    form = AdminPackageForm(request.POST or None)
    context = {'form': form}
    if request.method == "POST":
        if form.is_valid():
            new_package = form.save(commit=False)
            new_package.save()
            return redirect('/accounts/home/')
    return render(request, 'admin_create_package.html', context)


def ups_account_create(request):
    form = UPSAccountForm(request.POST or None)
    context = {'form': form}
    if request.method == "POST":
        if form.is_valid():
            new_package = form.save(commit=False)
            new_package.save()
            return redirect('/accounts/home/')
    return render(request, 'admin_create_ups_account.html', context)


def package_edit(request, package_id):
    if request.method != "POST":
        package = Package.objects.get(package_id=package_id)
        package_form = PackageForm(instance=package)
        context = {'package_id': package_id, 'form': package_form}
        return render(request, 'package_edit.html', context)
    else:
        # this will be reached when the user presses the save button
        form = PackageForm(request.POST or None)
        if form.is_valid():
            existing_package = Package.objects.get(package_id=package_id)
            package_form = PackageForm(request.POST, instance=existing_package)
            package_form.save()
            return redirect('/accounts/home/')

# UPSAccount(user)

def register(request):
    form = UserSignUpForm
    if request.method == "POST" :
        form = UserSignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("User is being saved")
            messages.success(request, "Registration successful.")
            new_ups_account = UPSAccount(user=user, world_id=0, acct_number=user.id)
            new_ups_account.save()
            return redirect("/login/")
    context = { 'form': form, 'messages': messages }
    return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, f"Logged in as {username}.")
                return redirect("/accounts/home/")
            else:
                messages.error(request, "Incorrect Username or Password")
        else:
            messages.error(request, "Incorrect Username or Password")
    form = AuthenticationForm(request, data=request.POST)
    return render(request=request, template_name="login_user.html", context={"login_form": form})


def logout_user(request):
    print(f"request.method -- {request.method}")
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            messages.success(request, "You have successfully logged out")
            logout(request)
            # request.session.flush()
            # request.user = AnonymousUser
            print(f"Changed request.user to {request.user}")
        else:
            messages.error(request, "Bad request. Please login again")
    return redirect("home")

