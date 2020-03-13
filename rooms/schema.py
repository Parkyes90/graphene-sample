import graphene

from .models import Room
from .types import RoomListType, RoomType


class Query(graphene.ObjectType):
    all_rooms = graphene.Field(RoomListType, page=graphene.Int(required=True))
    room = graphene.Field(RoomType, pk=graphene.ID(required=True))

    def resolve_room(self, info, pk):
        query = Room.objects.get(pk=pk)
        return query

    def resolve_all_rooms(self, info, page=1):
        page_size = 20
        if page < 1:
            page = 1
        queryset = Room.objects.all()

        return RoomListType(
            arr=queryset[(page - 1) * page_size : page * page_size],
            total=queryset.count(),
        )
