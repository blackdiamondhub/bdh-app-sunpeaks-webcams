from bdh_sdk import PluginSpec, Tile
from bdh_sdk.plugins import LIFECYCLE_ON_DEMAND, NETWORK_OUTBOUND
from bdh_sdk.provides import LIVE, SAVER, SaverSource

spec = PluginSpec(
    id="sunpeaks_webcams",
    app="sunpeaks_webcams",
    urls="sunpeaks_webcams.urls",
    provides={SAVER: "sunpeaks_webcams.provides.saver"},
    saver_sources=(SaverSource("cams", "Mountain cams", "Live webcams from around Sun Peaks", LIVE),),
    tiles=(
        Tile(
            title="Webcams",
            url_name="webcams",
            icon="sunpeaks_webcams/hub/icon.svg",
            section="mountain",
            subtitle="Live mountain views",
            order=30,
        ),
    ),
    api_version=2,
    # Uses no hub services: it only scrapes the resort's public webcam page.
    permissions=(),
    # Fetches the webcam page and images from sunpeaksresort.com.
    network=NETWORK_OUTBOUND,
    # The feed is fetched lazily on request, so nothing runs in the background.
    lifecycle=LIFECYCLE_ON_DEMAND,
    memory_mb=96,
)