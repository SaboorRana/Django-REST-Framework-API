from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        return data
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name','id']
class PersonSerializer(serializers.ModelSerializer):
    color= ColorSerializer()
    color_country=serializers.SerializerMethodField()
    class Meta:
        model=Person
        fields = '__all__'
    def get_color_country(self, obj):
        color_f = obj.color
        if color_f is None:
            return None
        return {'color':color_f.color_name, 'id':color_f.id,'country': 'Pakistan'}
    def validate(self, data):
        special_char = ['@', '#', '$', '%', '^', '&', '*']
        if any(c in special_char for c in data['first_name']):
            raise serializers.ValidationError("First name cannot contain special characters")
        """ if data['age'] < 18:
            raise serializers.ValidationError("Age must be greater than 18")
        """
        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self,data):
        if data["username"]:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username already exists.")
        
        if data["email"]:
            if User.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError("Email already exists.")
        return data 
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
        