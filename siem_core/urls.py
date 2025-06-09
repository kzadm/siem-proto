from django.urls import path
from .views import dashboard, add_event_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path("add-event/", add_event_view, name="add_event"),
]
