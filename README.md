[Ссылка на проект pythonanywhere ](http://yurchik.pythonanywhere.com)

[Ссылка на Docker Hub](https://hub.docker.com/repository/docker/ydtalel/web_app/general)


# запросы через интерфейс на Django Templates
```
/login/
```
Авторизация по номеру телефона, она же главная страница.
```
/verify-code-template/
```
подтверждение кода
```
/profile-template/
```
профиль пользователя,  ввод инвайт-кода, список приглашеннных пользователей

# запросы через API
API предоставляет функционал для авторизации по номеру телефона и управления инвайт-кодами.

## Ресурсы
## Профиль пользователя

Этот ресурс предоставляет информацию о профиле пользователя.
### Запрос

```
GET /profiles/ID/
```
## Получить информацию о текущем пользователе.
### Ответ

json
```
{
    "phone_number": "+79034567100",
    "invite_code": "RRCZ99",
    "referred_by": 25
}
```
## Авторизация по номеру телефона

Этот ресурс позволяет отправить код подтверждения на указанный номер телефона.
### Запрос

```
POST /send-verification-code/
```
### Отправить код подтверждения на номер телефона.

### Пример тела запроса:

json
```
{
    "phone_number": "+79034567000"
}
```
### Ответ

json
```
{
    "status": "sent",
    "message": "Verification code sent.",
    "verification_code": "8335"
}
```
### Подтверждение кода

Этот ресурс позволяет подтвердить код подтверждения и создать профиль пользователя, если его нет.
### Запрос
```
PUT /verify-code/
```
## Подтвердить код подтверждения.

### Пример тела запроса:

json
```
{
  "phone_number": "+79034567000",
  "verification_code": "4296"
}
```
### Ответ

json
```
{
    "status": "success",
    "message": "Verification successful."
}
```
## Активация инвайт-кода

Этот ресурс позволяет активировать инвайт-код пользователя.
### Запрос
```
POST /profiles/ID/activate_invite/
```
## Активировать инвайт-код.

### Пример тела запроса:

json
```
{
    "invite_code": "OBEHT5"
}
```
### Ответ

json
```
{
    "status": "success",
    "message": "Invite code activated."
}
```
## Список приглашенных пользователей

Этот ресурс предоставляет список пользователей, которые ввели инвайт-код текущего пользователя.
### Запрос

```
GET /profiles/ID/referred_users/
```
## Получить список приглашенных пользователей.
### Ответ

json
```
{
    "referred_users": [
        {
            "phone_number": "+79034567100"
        },
        {
            "phone_number": "+79934567200"
        }
    ]
}
```
## Пример использования

Отправьте POST запрос на /send-verification-code/ с телефонным номером для получения кода подтверждения.

Отправьте PUT запрос на /verify-code/ с номером телефона и подтверждающим кодом.

Получите профиль пользователя, отправив GET запрос на /profiles/ID/.

Активируйте инвайт-код, отправив POST запрос на /profiles/ID/activate_invite/ с инвайт-кодом.

Получите список приглашенных пользователей, отправив GET запрос на /profiles/ID/referred_users/.

