from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biz.urls")),
    path("token-auth/", obtain_jwt_token),
    path("api/user/", include("user.urls")),
]
