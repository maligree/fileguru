from core.models import UserAgent


def log_user_agent(get_response):
    def middleware(request):
        if not request.user.is_anonymous:
            user_agent_value = request.META.get(
                "HTTP_USER_AGENT", "<missing User-Agent header>"
            )

            obj, _ = UserAgent.objects.update_or_create(
                user=request.user, defaults={"value": user_agent_value}
            )

        return get_response(request)

    return middleware
