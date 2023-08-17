from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import UserProfile, VerificationCode
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import random
import time
import string


def home(request):
    return HttpResponse('Hello world')


@csrf_exempt  # удалить перед запуском
def profile(request):
    phone_number = request.GET.get('phone_number')
    user = get_object_or_404(UserProfile, phone_number=phone_number)

    if request.method == 'GET':
        data = {
            'phone_number': user.phone_number,
            'invite_code': user.invite_code,
            'referred_by': user.referred_by.phone_number if user.referred_by else None
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        new_invite_code = request.PUT.get('invite_code')  # Получаем новое значение инвайт-кода

        if user.invite_code and new_invite_code:
            return JsonResponse({'status': 'error', 'message': 'Invite code already exists.'})
        elif new_invite_code:
            user.invite_code = new_invite_code
            user.save()
            return JsonResponse({'status': 'updated', 'message': 'Invite code updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'New invite code is empty.'})

    return HttpResponse('Invalid request method.')


@csrf_exempt  # удалить перед запуском
def activate_invite(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        invite_code = request.POST.get('invite_code')

        try:
            referred_by_user = UserProfile.objects.get(invite_code=invite_code)
        except ObjectDoesNotExist:
            referred_by_user = None

        user, created = UserProfile.objects.get_or_create(phone_number=phone_number)

        if created:
            verification_code = ''.join(random.choices('0123456789', k=4))
            VerificationCode.objects.create(user=user, code=verification_code)

            invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user.invite_code = invite_code

            # Установка связи с реферрером
            user.referred_by = referred_by_user
            user.save()

            time.sleep(2)

            return JsonResponse({'status': 'created', 'message': 'Verification code sent.'})
        else:
            return JsonResponse({'status': 'exists', 'message': 'User already exists.'})

    return HttpResponse('Invalid request method.')


def referral_list(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        user = get_object_or_404(UserProfile, phone_number=phone_number)

        referred_users = UserProfile.objects.filter(referred_by=user)

        user_list = [{'phone_number': referred_user.phone_number} for referred_user in referred_users]

        return JsonResponse({'referred_users': user_list})

    return HttpResponse('Invalid request method.')
