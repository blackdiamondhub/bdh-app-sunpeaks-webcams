"""The webcams as a live screen saver source ("Mountain cams")."""
from bdh_sdk.provides import SaverImage
from django.urls import reverse

REFRESH_SECONDS = 60


def build_images(cams):
    """One image per camera, Sunburst first; each URL always shows the newest capture."""
    cams = sorted((c for c in cams if c.get("slug")),
                  key=lambda c: "sunburst" not in (c.get("camera_name") or "").lower())
    return [SaverImage("cams", c["slug"], reverse("webcam_latest", args=[c["slug"]]),
                       label=c.get("camera_name") or c["slug"], refresh_seconds=REFRESH_SECONDS)
            for c in cams]


def saver():
    from .views import feed

    cams, _wait = feed.get()
    return build_images(cams)
