import graphene

import rooms.schema
import users.schema


class Query(rooms.schema.Query, users.schema.Query, graphene.ObjectType):
    pass


class Mutation:
    pass


schema = graphene.Schema(query=Query)
