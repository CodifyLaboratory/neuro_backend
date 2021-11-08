from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from neuro import settings
from .models import User, City, Country, UserProfile, Gender


class UserTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(UserTokenSerializer, self).validate(attrs)
        email = attrs.get('email', '')
        user = User.objects.get(email=email)
        if not user.is_simple_user:
            raise serializers.ValidationError('This email already taken.')
        data.update({'is_simple_user': self.user.is_simple_user})
        data.update({'user_id': self.user.id})
        data.update({'time_access': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']})
        data.update({'time_refresh': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']})
        return data


class AdminTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(AdminTokenSerializer, self).validate(attrs)
        email = attrs.get('email', '')
        user = User.objects.get(email=email)
        if not user.is_professor:
            raise serializers.ValidationError('This email is already taken.')
        data.update({'is_professor': self.user.is_professor})
        data.update({'user_id': self.user.id})
        data.update({'user_email': self.user.email})
        data.update({'time_access': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']})
        data.update({'time_refresh': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']})
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'confirm_password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Password mismatch.')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'confirm_password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Password mismatch.')
        user = User.objects.create_admin(password=password, **validated_data)
        return user


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class UserProfileSerializer(WritableNestedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'gender', 'age', 'phone', 'country', 'city']


class UserProfileListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    country = CountrySerializer(many=False, read_only=True)
    city = CountrySerializer(many=False, read_only=True)
    gender = GenderSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'gender', 'age', 'phone', 'country', 'city']


class UserSerializer(WritableNestedModelSerializer):
    user_profile = UserProfileSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'user_profile']


class UserListSerializer(serializers.ModelSerializer):
    user_profile = UserProfileListSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'user_profile']