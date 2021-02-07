from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('about/author/', views.AboutPage.as_view(), name='about'),
    path('about/tech/', views.TechPage.as_view(), name='tech')
]
