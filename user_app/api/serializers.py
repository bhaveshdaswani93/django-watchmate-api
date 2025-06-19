from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data.get('password2', None)

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        
        if User.objects.filter(username=user.username).exists():
            raise serializers.ValidationError("Username already exists")
        
        if User.objects.filter(email=user.email).exists():
            raise serializers.ValidationError("Email already exists")

        user.set_password(password)
        user.save()
        return user