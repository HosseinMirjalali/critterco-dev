from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("api/user/", include("user.urls")),
    url(
        r"^api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
