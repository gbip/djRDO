from djRDO import settings


def registration_enabled(request):
    return {"registration_enabled": settings.REGISTRATION_ENABLED}


def demo_enabled(request):
    return {"demo_enabled": settings.DEMO_ENABLED}
