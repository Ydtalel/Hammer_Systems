from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile

import string
import random
import time


def menu_root(request):
    return render(request, 'referrals/menu.html')


def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Генерация и сохранение кода подтверждения в сессии
        verification_code = ''.join(random.choices('0123456789', k=4))
        request.session['verification_code'] = verification_code
        request.session['phone_number'] = phone_number
        time.sleep(2)

        return redirect('verify-code')  # Переход на страницу ввода кода

    return render(request, 'referrals/login.html')


def verify_code_view(request):
    phone_number = request.session.get('phone_number')
    generated_code = request.session.get('verification_code')

    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')

        if generated_code == entered_code:
            user, created = UserProfile.objects.get_or_create(phone_number=phone_number)

            if created:
                # Генерация и сохранение инвайт-кода для нового пользователя
                invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                user.invite_code = invite_code
                user.save()

            # Очистка сессии от кода подтверждения
            del request.session['verification_code']

            return redirect('profile')
        else:
            messages.error(request, 'Invalid verification code. Please enter the correct code.')

    return render(request, 'referrals/verify_code.html',
                  {'phone_number': phone_number, 'generated_code': generated_code})


def profile_view(request):
    user = get_object_or_404(UserProfile, phone_number=request.session.get('phone_number'))

    if user.referred_by:
        invite_status = 'activated'
    else:
        invite_status = 'not_activated'

    invite_code = ''
    invite_error = ''
    invitees = None  # Создаем переменную для хранения списка приглашенных

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')

        if invite_code and invite_status == 'not_activated' and user.referred_by is None:
            if invite_code == user.invite_code:
                invite_error = "You cannot use your own invite code."
            else:
                try:
                    referred_by_user = UserProfile.objects.get(invite_code=invite_code)
                    user.referred_by = referred_by_user
                    user.save()
                    messages.success(request, 'Invite code activated successfully.')
                    invite_status = 'activated'
                except ObjectDoesNotExist:
                    invite_error = 'Invalid invite code.'

    # Получаем список приглашенных для текущего пользователя, если он есть
    if user.referred_by:
        invitees = UserProfile.objects.filter(referred_by=user)

    return render(request, 'referrals/profile.html', {
        'user': user,
        'invite_status': invite_status,
        'invite_code': invite_code,
        'invite_error': invite_error,
        'invitees': invitees,
    })


