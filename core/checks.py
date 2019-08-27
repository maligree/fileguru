from django.conf import settings
from django.core.checks import Warning, register
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


@register()
def check_base_app_url_configured(app_configs, **kwargs):
    url_validator = URLValidator()
    try:
        url_validator(settings.BASE_APP_URL)
    except ValidationError as e:
        # Has to be a list, mind the hack.
        return [
            Warning(
                "BASE_APP_URL is not a valid URL. Some API methods may return erroneous fields.",
                hint="Set it to wherever your app lives, e.g. https://fileguru.com",
                id="core.W001",
            )
        ]

    return []  # Gotta be done ¯\_(ツ)_/¯
