from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('about-us/', TemplateView.as_view(template_name='main/about_us.html'), name='about_us'),
    path('contact-us/', TemplateView.as_view(template_name='main/contact_us.html'), name='contact_us'),
]