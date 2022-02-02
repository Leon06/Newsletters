from django.urls import path
from .import views

app_name="newsletters"

urlpatterns = [
    path('entrenamiento/',views.newsletter_signup, name="optin"),
    path('unsubscribe/',views.newsletter_unsubscribe, name="unsubscribe"),
]
