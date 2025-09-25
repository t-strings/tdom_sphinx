from tdom import Node, html

from tdom_sphinx.models import TdomContext


def Head(*, context: TdomContext) -> Node:
    pathto = context.page_context["pathto"]
    site_title = context.page_context["site_title"]
    title = context.page_context["title"]
    if site_title is None:
        full_title = f"{title}"
    else:
        full_title = f"{title} - {site_title}"

    return html(t'''
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{full_title}</title>
  <link rel="stylesheet" href="{pathto("_static/pico.css", 1)}" />
  <link rel="stylesheet" href="{pathto("_static/sphinx.css", 1)}" />
  <link rel="icon" href="{pathto("_static/favicon.ico", 1)}" type="image/x-icon" />
</head>
''')
