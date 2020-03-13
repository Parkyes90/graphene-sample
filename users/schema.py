import graphene

from .mutations import CreateAccountMutation
from .types import UserArrayType, UserType
from .queries import resolve_user, resolve_all_users


class Query(object):
    all_users = graphene.Field(
        UserArrayType, page=graphene.Int(), resolver=resolve_all_users
    )
    user = graphene.Field(
        UserType, pk=graphene.ID(required=True), resolver=resolve_user
    )


class Mutation(object):
    create_account = CreateAccountMutation.Field()
