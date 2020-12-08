import os

from aiohttp import web
from .partify import partify


async def partify_image(request):
    request_body = await request.post()
    try:
        result = partify(request_body['image'].file.read())
    except AttributeError:
        return web.json_response({'error': 'Missing image'}, status=400)
    except IOError:
        return web.json_response({'error': 'Image could not be processed'}, status=400)

    return web.Response(body=result, headers={'content-type': 'image/gif'})


async def index(request):
    return web.FileResponse('./static/index.html')


def main():
    app = web.Application()

    app.router.add_route('GET', '/', index, name='index')
    app.router.add_route('POST', '/api/partify', partify_image, name='partify')

    port = int(os.environ.get("PORT", 3333))
    web.run_app(app, port=port)
