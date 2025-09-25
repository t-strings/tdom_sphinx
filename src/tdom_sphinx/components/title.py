from tdom import html


def Title(page_title: str, site_title: str | None = None):
    if site_title is None:
        full_title = f"{page_title}"
    else:
        full_title = f"{page_title} - {site_title}"

    return html(t"<title>{full_title}</title>")
