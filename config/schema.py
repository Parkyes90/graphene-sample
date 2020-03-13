import graphene
from graphene_django import DjangoObjectType

import rooms.schema


class Query(rooms.schema.Query, graphene.ObjectType):
    pass


class Mutation:
    pass


schema = graphene.Schema(query=Query)
