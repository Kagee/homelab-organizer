import logging
from urllib.parse import urlparse

from workers import Response, handler

HOSTS = {
    "bc.h2x.no": "hlo.h2x.no",
    "bcd.h2x.no": "hlo-dev.intern.hild1.no",
}
SHAANDSLASH = 41  # /<sha1>


@handler
async def on_fetch(request, _env):
    path = urlparse(request.url).path

    if len(path) != SHAANDSLASH or request.headers["Host"] not in HOSTS:
        return Response("", status=403)

    try:
        _ = int(path[1:], 16)
    except ValueError:
        return Response("", status=403)

    # 307 Temporary Redirect (keep protocol (POST,GET etc)
    return Response.redirect(
        f"https://{HOSTS[request.headers['host']]}/{path[1:].upper()}",
        307,
    )
