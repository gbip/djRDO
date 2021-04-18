from django.http import HttpResponseRedirect


def redirect_to_referer_or(request, default):
    if referer := request.META.get("HTTP_REFERER") is not None:
        return HttpResponseRedirect(
            referer
        )
    else:
        return default
