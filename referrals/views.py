from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import UserProfile, VerificationCode
from .serializers import UserProfileSerializer

import random
import time
import string


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]  # Настройте права доступа по своим требованиям

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_invite_code = request.data.get('invite_code')

        if instance.invite_code and new_invite_code:
            return Response({'status': 'error', 'message': 'Invite code already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif new_invite_code:
            instance.invite_code = new_invite_code
            instance.save()
            return Response({'status': 'updated', 'message': 'Invite code updated.'})
        else:
            return Response({'status': 'error', 'message': 'New invite code is empty.'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def activate_invite(request):
    if request.method == 'POST':
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')

        try:
            referred_by_user = UserProfile.objects.get(invite_code=invite_code)
        except UserProfile.DoesNotExist:
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

            return Response({'status': 'created', 'message': 'Verification code sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'exists', 'message': 'User already exists.'}, status=status.HTTP_200_OK)

    return Response({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def referral_list(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        user = get_object_or_404(UserProfile, phone_number=phone_number)

        referred_users = UserProfile.objects.filter(referred_by=user)

        user_list = [{'phone_number': referred_user.phone_number} for referred_user in referred_users]

        return Response({'referred_users': user_list})

    return Response({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
