from enum import Enum


class TryItCredentialPolicyOptions(Enum):
    OMIT = "omit"
    INCLUDE = "include"
    SAME_ORIGIN = "same-origin"


class LayoutOptions(Enum):
    SIDEBAR = "sidebar"
    RESPONSIVE = "responsive"
    STACKED = "stacked"


class RouterOptions(Enum):
    HISTORY = "history"
    HASH = "hash"
    MEMORY = "memory"
    STATIC = "static"


def get_stoplight_elements_html(  # noqa: PLR0913 many arguments in function definition
    *,
    openapi_url: str,
    title: str,
    stoplight_elements_js_url: str = "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js",
    stoplight_elements_css_url: str = "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css",
    stoplight_elements_favicon_url: str = "https://docs.stoplight.io/favicons/favicon.ico",
    api_description_document: str = "",
    base_path: str = "",
    hide_internal: bool = False,
    hide_try_it: bool = False,
    hide_export: bool = False,
    try_it_cors_proxy: str = "",
    try_it_credential_policy: TryItCredentialPolicyOptions = TryItCredentialPolicyOptions.OMIT,
    layout: LayoutOptions = LayoutOptions.SIDEBAR,
    logo: str = "",
    router: RouterOptions = RouterOptions.HASH,
) -> str:
    """
    Generate an HTML document that embeds the Stoplight Elements API Explorer.

    https://docs.stoplight.io/docs/elements/b074dc47b2826-elements-configuration-options

    Args:
        openapi_url: OpenAPI document URL, supporting `http://`, `https://`, and documents containing `$ref` to other http(s) documents.
        title: The title of the HTML document.
        stoplight_elements_js_url: URL to the Stoplight Elements JavaScript file.
        stoplight_elements_css_url: URL to the Stoplight Elements CSS file.
        stoplight_elements_favicon_url: URL to the Stoplight Elements favicon.
        api_description_document: OpenAPI document, provided as YAML string, JSON string, or JavaScript object.
        base_path: Helps when using `router: 'history'` but docs are in a subdirectory like `https://example.com/docs/api`.
        hide_internal: Pass `True` to filter out any content which has been marked as internal with `x-internal`.
        hide_try_it: Pass `True` to hide the [Try It feature](https://docs.stoplight.io/docs/platform/ZG9jOjM2OTM3Mjky-try-it).
        hide_export: Pass `True` to hide the Export button on overview section of the documentation.
        try_it_cors_proxy: Pass the URL of a CORS proxy used to send requests to the Try It feature. The provided URL is pre-pended to the URL of an actual request.
        try_it_credential_policy: Use to fetch the credential policy for the Try It feature. Options are: `omit` (default), `include`, and `same-origin`.
        layout: There are three layouts for Elements:
          - `sidebar` - (default) Three-column design with a sidebar that can be resized.
          - `responsive` - Like `sidebar`, except at small screen sizes it collapses the sidebar into a drawer that can be toggled open.
          - `stacked` - Everything in a single column, making integrations with existing websites that have their own sidebar or other columns already.
        logo: URL to an image that displays as a small square logo next to the title, above the table of contents.
        router:  Determines how navigation should work:
          - `history` - uses the HTML5 history API to keep the UI in sync with the URL.
          - `hash` - (default) uses the hash portion of the URL to keep the UI in sync with the URL.
          - `memory` - keeps the history of your "URL" in memory (doesn't read or write to the address bar).
          - `static` - renders using the StaticRouter which can help render pages on the server.

    Returns:
        The HTML document as a string.
    """

    return f"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{title}</title>

    {f'<link rel="shortcut icon" href="{stoplight_elements_favicon_url}">' if stoplight_elements_favicon_url else ""}
    <script src="{stoplight_elements_js_url}"></script>
    <link rel="stylesheet" href="{stoplight_elements_css_url}">
  </head>
<body>
  <elements-api
    {f'apiDescriptionUrl="{openapi_url}"' if openapi_url else ""}
    {f'apiDescriptionDocument="{api_description_document}"' if api_description_document else ""}
    {f'basePath="{base_path}"' if base_path else ""}
    {'hideInternal="true"' if hide_internal else ""}
    {'hideTryIt="true"' if hide_try_it else ""}
    {'hideExport="true"' if hide_export else ""}
    {f'tryItCorsProxy="{try_it_cors_proxy}"' if try_it_cors_proxy else ""}
    tryItCredentialPolicy="{try_it_credential_policy.value}"
    layout="{layout.value}"
    {f'logo="{logo}"' if logo else ""}
    router="{router.value}"
  />
</body>
</html>
"""
