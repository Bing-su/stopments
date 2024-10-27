import base64 as _base64
import zlib as _zlib

from .favicon import content as _favicon
from .styles import content as _styles
from .web_components import content as _web_components


def _decode(content: str) -> bytes:
    z = _base64.b85decode(content)
    return _zlib.decompress(z)


favicon = _decode(_favicon)
"image/x-icon"

css_content = _decode(_styles)
"text/css; charset=utf-8"

js_content = _decode(_web_components)
"application/javascript; charset=utf-8"
