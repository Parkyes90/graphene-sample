import graphene

import rooms.schema
import users.schema


class Query(rooms.schema.Query, users.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
