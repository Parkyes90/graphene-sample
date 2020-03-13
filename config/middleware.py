import jwt
from django.conf import settings

from users.models import User


class JWTMiddleware(object):
    def resolve(self, _next, root, info, **kwargs):
        request = info.context
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return _next(root, info, **kwargs)
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            info.context.user = user
        except Exception as e:
            print(e)
        return _next(root, info, **kwargs)
