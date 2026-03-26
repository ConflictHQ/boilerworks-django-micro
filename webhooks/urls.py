from django.urls import path

from . import views

urlpatterns = [
    path("", views.WebhookReceiveView.as_view(), name="webhook-receive"),
    path("events/", views.WebhookListView.as_view(), name="webhook-list"),
    path("events/<uuid:guid>/", views.WebhookDetailView.as_view(), name="webhook-detail"),
]
