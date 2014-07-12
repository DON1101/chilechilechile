import settings


def site_metadata():
    """
    Metadata related to settings of the whole site.
    This is used in HTTP response.
    """

    site_metadata = dict(
        SITE_NAME=settings.SITE_NAME,
        SITE_HTTP_URL=settings.SITE_HTTP_URL,
    )
    return site_metadata
