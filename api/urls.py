from django.urls import path

from . import views

urlpatterns = [
    path("keys/", views.ApiKeyListCreateView.as_view(), name="api-keys"),
    path("keys/<uuid:guid>/", views.ApiKeyRevokeView.as_view(), name="api-key-revoke"),
]
