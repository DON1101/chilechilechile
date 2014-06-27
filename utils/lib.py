import pytz
import tzlocal


def convert_to_time_zone(src_datetime,
                         dest_timezone="",
                         src_timezone=tzlocal.get_localzone().zone):
    src_tz = pytz.timezone(src_timezone)
    dest_tz = pytz.timezone(dest_timezone)

    src_datetime_utc = src_tz.localize(
        src_datetime, is_dst=None
    ).astimezone(pytz.utc)
    dest_datetime_utc = src_datetime_utc.replace(
        tzinfo=pytz.utc
    ).astimezone(dest_tz)

    dest_datetime = dest_tz.normalize(dest_datetime_utc)

    return dest_datetime
