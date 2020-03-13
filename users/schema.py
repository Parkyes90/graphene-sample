import graphene

from .mutations import (
    CreateAccountMutation,
    LoginMutation,
    ToggleFavsMutation,
    EditProfileMutation,
)
from .types import UserArrayType, UserType
from .queries import resolve_user, resolve_all_users, resolve_me


class Query(object):
    all_users = graphene.Field(
        UserArrayType, page=graphene.Int(), resolver=resolve_all_users
    )
    user = graphene.Field(
        UserType, pk=graphene.ID(required=True), resolver=resolve_user
    )

    me = graphene.Field(UserType, resolver=resolve_me)


class Mutation(object):
    create_account = CreateAccountMutation.Field()
    login = LoginMutation.Field()
    toggle_favs = ToggleFavsMutation.Field()
    edit_profile = EditProfileMutation.Field()
