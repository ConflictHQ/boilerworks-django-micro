from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

admin.site.site_header = "Boilerworks Micro"
admin.site.site_title = "Boilerworks Micro Admin"


def health_check(request):
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=503)


urlpatterns = [
    path("health/", health_check, name="health"),
    path("api/", include("api.urls")),
    path("api/webhooks/", include("webhooks.urls")),
    path("admin/", admin.site.urls),
]
