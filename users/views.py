import json
import re
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from json.decoder           import JSONDecodeError
from django.conf            import settings

from users.models           import User

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            phone_number = data.get('phone_number')
            name         = data.get('name') 
            address      = data.get('address')

            REGEX_EMAIL    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            REGEX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if not re.match(re.compile(REGEX_EMAIL), email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)

            if not re.match(re.compile(REGEX_PASSWORD), password):
                return JsonResponse({'message : INVAILD_PASSWORD'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EMAIL_ALREADY_EXISTS'}, status=400)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_password,
                phone_number = phone_number,
                address      = address,
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return  JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'USER_DOSE_NOT_EXIST'}, status=404)

            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
            
            token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'token':token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSOND_DECODE_ERROR'}, status = 400)

