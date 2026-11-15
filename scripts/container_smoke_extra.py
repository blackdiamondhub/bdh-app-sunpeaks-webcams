"""Load every thumbnail at once, like the page does, to check the
downscaling of 3-4K originals fits in the container's memory limit."""
import json
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from bdh_sdk.identity import signed_headers


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


opener = urllib.request.build_opener(NoRedirect)


def get(path):
    req = urllib.request.Request(
        "http://127.0.0.1:8000" + path,
        headers=signed_headers(os.environ["BDH_APP_TOKEN"], "GET", path),
    )
    with opener.open(req, timeout=60) as resp:
        return resp.status, resp.headers.get("Content-Type"), resp.read()


_, _, body = get("/sunpeaks_webcams/get_webcams/")
cams = json.loads(body)["webcams"]
paths = [f"/sunpeaks_webcams/thumb/{c['slug']}/{c['timestamp']}.jpg" for c in cams if c.get("timestamp")]
assert paths, "no cameras with captures"
with ThreadPoolExecutor(8) as pool:
    results = list(pool.map(get, paths))
for path, (status, ctype, data) in zip(paths, results):
    print(status, ctype, len(data), "bytes", path)
    assert status == 200 and ctype == "image/jpeg", path