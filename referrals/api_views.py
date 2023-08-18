from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserProfileSerializer

import string
from django.core.cache import cache
import random


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    # Действие для отправки кода подтверждения на указанный номер телефона
    @action(detail=False, methods=['POST'])
    def send_verification_code(self, request):
        phone_number = request.data.get('phone_number')

        # Генерируем случайный 4-значный код подтверждения
        verification_code = ''.join(random.choices('0123456789', k=4))

        # Сохраняем код подтверждения в кэше с тайм-аутом 10 минут
        cache.set(f'verification_code_{phone_number}', verification_code, timeout=600)

        return Response(
            {'status': 'sent', 'message': 'Verification code sent.', 'verification_code': verification_code},
            status=status.HTTP_201_CREATED)

    # Действие для проверки введенного кода подтверждения и создания пользователя
    @action(detail=False, methods=['PUT'])
    def verify_code(self, request):
        phone_number = request.data.get('phone_number')
        entered_code = request.data.get('verification_code')

        cached_code = cache.get(f'verification_code_{phone_number}')

        if cached_code == entered_code:
            # Получаем или создаем пользователя на основе номера телефона
            user, created = UserProfile.objects.get_or_create(phone_number=phone_number)

            if created:
                # Генерируем случайный 6-значный инвайт-код для нового пользователя
                invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                user.invite_code = invite_code
                user.save()

            return Response({'status': 'success', 'message': 'Verification successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Invalid verification code.'},
                            status=status.HTTP_400_BAD_REQUEST)

    # Действие для получения информации о профиле пользователя
    @action(detail=False, methods=['GET'])
    def profile(self, request):
        phone_number = request.data.get('phone_number')

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'phone_number': user.phone_number, 'invite_code': user.invite_code})

    # Действие для активации инвайт-кода текущим пользователем
    @action(detail=True, methods=['POST'])
    def activate_invite(self, request, pk=None):
        invite_code = request.data.get('invite_code')

        try:
            referred_by_user = UserProfile.objects.get(invite_code=invite_code)
        except UserProfile.DoesNotExist:
            return Response({'status': 'error', 'message': 'Invalid invite code.'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object()

        if user.referred_by:
            return Response({'status': 'error', 'message': 'Invite code already activated.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.referred_by = referred_by_user
        user.save()

        return Response({'status': 'success', 'message': 'Invite code activated.'}, status=status.HTTP_200_OK)

    # Действие для получения списка пользователей, которые использовали инвайт-код текущего пользователя
    @action(detail=True, methods=['GET'])
    def referred_users(self, request, pk=None):
        user = self.get_object()
        referred_users = UserProfile.objects.filter(referred_by=user)

        user_list = [{'phone_number': referred_user.phone_number} for referred_user in referred_users]

        return Response({'referred_users': user_list})