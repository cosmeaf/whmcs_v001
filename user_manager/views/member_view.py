# user_manager/views/member_view.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_manager.models import Member

@login_required(login_url='account_login')
def member_list(request):
    member = get_object_or_404(Member, user=request.user)
    return render(request, 'dashboard/member_list.html', {'member': member})


@login_required(login_url='account_login')
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        # Exclui apenas o Member, não o User
        member.delete()
        messages.success(request, 'Sua conta de membro foi excluída com sucesso.')
        return redirect('home')

    return render(request, 'modals/exclude_member.html', {'member': member})