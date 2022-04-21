from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from person.models import CustomeUser, ResetPasswordModel
import random, string


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = ('__all__')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if validated_data['password'] is not None:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


# with user credentials
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password'] and instance.check_password(
                validated_data['old_password']):
            # instance.password = validated_data['new_password']
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
        return instance


# class PasswordChangeSerializer(serializers.Serializer):
#     old_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#
#     def validate_old_password(self, value):
#         request = self.context.get("request")
#         user = request.user
#         if not user.check_password(value):
#             raise serializers.ValidationError(_("Incorrect password"))
#         return value
#
#     def validate(self, data):
#         if data["new_password"] != data.pop("confirm_password"):
#             raise serializers.ValidationError({"password": _("Passwords don't match.")})
#         try:
#             validate_password(data["new_password"])
#         except Exception as e:
#             raise serializers.ValidationError({"password": e}) from e
#         return data
#
#     def save(self, **kwargs):
#         request = self.context.get("request")
#         user = request.user
#         user.set_password(self.validated_data["new_password"])
#         user.save()
#         return user


class SendEmailForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordModel
        fields = ['email', 'password']


# without user credentials
class ChangePasswordWithoutCredentialsSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def update(self, instance, validated_data):

        # instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'not found'})

        # if not instance.check_password(validated_data['old_password']):
        #     raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password']:
            # instance.password = validated_data['new_password']
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
        else:
            return serializers.ValidationError('can not detect')
