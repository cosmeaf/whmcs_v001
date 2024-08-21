from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_manager.models import Domain, Member
from user_manager.forms.domain_forms import DomainForm
from django.http import HttpResponse
import os 


@login_required(login_url='account_login')
def domain_list(request):
    # Filter domains to show only those belonging to the logged-in user
    domains = Domain.objects.filter(member=request.user.member)
    return render(request, 'dashboard/domain_list.html', {'domains': domains})


@login_required(login_url='account_login')
def domain_create(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.member = request.user.member

            try:
                domain.save()
                messages.success(request, 'Domínio criado com sucesso!')
                return redirect('domain_list')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = DomainForm()
    return render(request, 'dashboard/domain_form.html', {'form': form})



@login_required(login_url='account_login')
def domain_update(request, pk):
    domain = get_object_or_404(Domain, pk=pk, member=request.user.member)
    if request.method == 'POST':
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Domínio atualizado com sucesso!')
                return redirect('domain_list')
            except ValueError as e:
                messages.error(request, str(e))  # Show error message if quota is exceeded
    else:
        form = DomainForm(instance=domain)
    return render(request, 'dashboard/domain_form.html', {'form': form})



@login_required(login_url='account_login')
def domain_delete(request, pk):
    domain = get_object_or_404(Domain, pk=pk, member=request.user.member)
    if request.method == 'POST':
        domain.delete()
        messages.success(request, 'Domínio excluído com sucesso!')
        return redirect('domain_list')
    return render(request, 'dashboard/domain_confirm_delete.html', {'domain': domain})


@login_required
def file_manager_view(request):
    member = request.user.member
    directory_path = member.get_home_directory_path()
    
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        files.append({
            'name': filename,
            'url': file_path,
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        })

    return render(request, 'dashboard/file_manager.html', {
        'member': member,
        'files': files
    })
