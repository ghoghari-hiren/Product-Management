from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Product

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        validated_data['role'] = 'user'
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Both email and password are required")


class ProductSerializer(serializers.ModelSerializer):
    ssn = serializers.CharField(
        validators=[]
    )

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_on', 'updated_on', 'is_active']

    def validate_ssn(self, value):
        product = self.instance
        if Product.objects.exclude(pk=getattr(product, 'pk', None)).filter(ssn=value).exists():
            raise serializers.ValidationError("Product with this SSN already exists.")
        return value