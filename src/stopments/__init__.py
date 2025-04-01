from .__version__ import __version__
from .elements import (
    LayoutOptions,
    RouterOptions,
    TryItCredentialPolicyOptions,
    get_stoplight_elements_html,
)

# Literal strings for file names
WEB_COMPONENTS = "web-components.min.js"
"web-components.min.js"
STYLES = "styles.min.css"
"styles.min.css"
FAVICON = "favicon.ico"
"favicon.ico"

__all__ = [
    "FAVICON",
    "STYLES",
    "WEB_COMPONENTS",
    "LayoutOptions",
    "RouterOptions",
    "TryItCredentialPolicyOptions",
    "__version__",
    "get_stoplight_elements_html",
]
