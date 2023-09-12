from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import RegistrationUserForm, LoginUserForm, ProfileEditForm, UserEditForm


def sing_up(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        user_form = RegistrationUserForm(request.POST)
        if user_form.is_valid():
            #  Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit=False)
            #  Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            #  Сохранить объект User
            new_user.save()
            #  Создается связь между User и Profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/sign_up_done.html', {'new_user': new_user})
        else:
            #  Во время регистрации нового пользователя что-то пошло не так.
            messages.error(request, 'Error registration your account.')
    else:
        user_form = RegistrationUserForm()
    return render(request, 'account/sign_up.html', {'form': user_form})


def sign_in(request):
    """Вход в аккаунт"""
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #  Проверка набора учетных данных пользователя
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            return redirect('homepage')
    else:
        form = LoginUserForm()
    return render(request, 'account/sign_in.html', {'form': form})


def sign_out(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('homepage')


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    user_avatar = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form_profile = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        form_user = UserEditForm(instance=request.user,
                                 data=request.POST)
        if form_profile.is_valid() and form_user.is_valid():
            form_profile.save()
            form_user.save()
            return redirect('profile_edit')
    else:
        form_profile = ProfileEditForm(instance=request.user.profile)
        form_user = UserEditForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form_profile': form_profile,
                                                         'form_user': form_user,
                                                         'user_avatar': user_avatar})
