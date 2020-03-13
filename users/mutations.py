import graphene

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
