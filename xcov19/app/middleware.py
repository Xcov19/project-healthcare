from typing import Callable, Awaitable

from blacksheep import Application, Request, Response, bad_request

from xcov19.app.settings import FromOriginMatchHeader


def configure_middleware(app: Application, *middlewares):
    app.middlewares.extend(middlewares)


async def origin_header_middleware(
    request: Request, handler: Callable[[Request], Awaitable[Response]]
) -> Response:
    if not FromOriginMatchHeader.name:
        raise ValueError("FromOriginMatchHeader name is not set.")
    if request.path.startswith("/docs") or request.path.startswith("/openapi"):
        return await handler(request)
    match request.headers.get(FromOriginMatchHeader.name.encode()):
        case (b"secret",):
            return await handler(request)
        case _:
            return bad_request("Invalid origin match header value provided.")
