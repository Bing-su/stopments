from typing import Any

import pytest

from stopments import (
    LayoutOptions,
    RouterOptions,
    TryItCredentialPolicyOptions,
    get_stoplight_elements_html,
)


def test_get_stoplight_elements_html():
    openapi_url = "https://api.apis.guru/v2/specs/github.com/1.1.4/openapi.json"
    title = "GitHub v3 REST API"
    html = get_stoplight_elements_html(
        openapi_url=openapi_url,
        title=title,
    )

    assert isinstance(html, str)
    assert openapi_url in html
    assert title in html


@pytest.mark.parametrize(
    ("kwargs", "include_str"),
    [
        (
            {
                "stoplight_elements_js_url": "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js"
            },
            '"https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js"',
        ),
        (
            {
                "stoplight_elements_css_url": "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css"
            },
            '"https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css"',
        ),
        (
            {
                "stoplight_elements_favicon_url": "https://docs.stoplight.io/favicons/favicon.ico"
            },
            '"https://docs.stoplight.io/favicons/favicon.ico"',
        ),
        (
            {
                "api_description_document": "openapi: 3.0.0\ninfo:\n  title: Test API\n  version: 1.0.0\npaths: {}"
            },
            "apiDescriptionDocument",
        ),
        ({"base_path": "/docs/api"}, "basePath="),
        ({"hide_internal": True}, "hideInternal="),
        ({"hide_try_it": True}, "hideTryIt="),
        ({"hide_export": True}, "hideExport="),
        ({"try_it_cors_proxy": "https://cors-proxy.example.com"}, "tryItCorsProxy="),
        (
            {"try_it_credential_policy": TryItCredentialPolicyOptions.OMIT},
            'tryItCredentialPolicy="omit"',
        ),
        ({"layout": LayoutOptions.RESPONSIVE}, 'layout="responsive"'),
        ({"logo": "https://example.com/logo.png"}, "logo="),
        ({"router": RouterOptions.HASH}, 'router="hash"'),
    ],
)
def test_includes(kwargs: dict[str, Any], include_str: str):
    openapi_url = "https://api.apis.guru/v2/specs/github.com/1.1.4/openapi.json"
    title = "GitHub v3 REST API"
    html = get_stoplight_elements_html(
        openapi_url=openapi_url,
        title=title,
        **kwargs,
    )
    assert include_str in html
