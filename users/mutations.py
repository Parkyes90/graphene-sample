import graphene
import jwt
from django.conf import settings
from django.contrib.auth import authenticate

from rooms.models import Room
from .models import User


class CreateAccountMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, email, password, last_name="", first_name=""):
        try:
            User.objects.get(email=email)
            return CreateAccountMutation(ok=False, error="User already exists")
        except User.DoesNotExist:
            try:
                User.objects.create_user(
                    email=email,
                    username=email,
                    password=password,
                    last_name=last_name,
                    first_name=first_name,
                )
                return CreateAccountMutation(ok=True, error="")
            except Exception as e:
                return CreateAccountMutation(ok=False, error=str(e))


class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    pk = graphene.ID()
    error = graphene.String()

    def mutate(self, info, email, password):
        user = authenticate(info.context, username=email, password=password)
        if not user:
            return LoginMutation(error="유효하지 않은 계정 또는 비밀번호 입니다.")
        token = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return LoginMutation(token=token.decode("utf-8"), pk=user.pk)


class ToggleFavsMutation(graphene.Mutation):
    class Arguments:
        room_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, room_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You need to be logged in")

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return ToggleFavsMutation(ok=False, error="Room not founded")
        if room in user.favs.all():
            user.favs.remove(room)
        else:
            user.favs.add(room)
        return ToggleFavsMutation(ok=True)


class EditProfileMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, first_name=None, last_name=None, email=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You need to be logged in")

        try:
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if email is not None and email != user.email:
                try:
                    User.objects.get(email=email)
                    return EditProfileMutation(
                        ok=False, error="That email is taken"
                    )
                except User.DoesNotExist:
                    user.username = email
                    user.email = email

            user.save()
        except Exception as e:
            return EditProfileMutation(ok=True, error=str(e))
        return EditProfileMutation(ok=True)
