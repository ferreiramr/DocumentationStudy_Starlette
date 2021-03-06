import base64
import binascii
import re

import uvicorn
from starlette.applications import Starlette
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError, SimpleUser,
                                      requires)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route


class BasicAuthBackend(AuthenticationBackend):

    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode('ascii')
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        if username == "admin":
            # TODO: You'd want to verify the username and password here.
            return AuthCredentials(["authenticated"]), SimpleUser(username)


async def homepage(request):
    if request.user.is_authenticated:
        return PlainTextResponse('Hello ' + request.user.display_name)
    return PlainTextResponse('Hello, you')

@requires('authenticated')
async def dashboard(request):
    return PlainTextResponse('Dashboard')


routes = [
        Route("/", endpoint=homepage),
        Route("/dashboard", endpoint=dashboard)
    ]

middleware = [Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())]

app = Starlette(routes=routes, middleware=middleware)

uvicorn.run(app)
