from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from user_app import models
from user_app.api.serializers import RegisterUserSerializer

@api_view(['POST'])
def register_user(request):
    """
    Register a new user.
    """
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.filter(user=user).first()
            if token:
                data['token'] = token.key
            else:
                data['token'] = None

            data['message'] = 'User created successfully'
            data['user_id'] = user.id
        

            return Response(data, status=201)
        else:
          return Response(serializer.errors, status=400)
    return Response({"error": "Invalid request method"}, status=405)
