from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect

@login_required(login_url='account_login')
def dashboard_view(request):
    return redirect('member_list')

@login_required(login_url='account_login')
def logout_view(request):
    logout(request)
    return redirect('account_login')