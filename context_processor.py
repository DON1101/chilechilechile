import settings


def site_metadata():
    """
    Metadata related to settings of the whole site.
    This is used in HTTP response.
    """

    site_metadata = dict(
        SITE_NAME=settings.SITE_NAME,
    )
    return site_metadata
