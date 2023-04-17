from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('save_instagram_credentials/', views.save_instagram_credentials, name='save_instagram_credentials'),
    path('home/', views.instagram_data, name='instagram_data'),
]