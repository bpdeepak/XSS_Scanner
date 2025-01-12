from django.urls import path
from .views import search, comments,dom_xss

urlpatterns = [
    path('', search, name='home'),         # Reflected XSS
    path('comments/', comments, name='comments'),  # Stored XSS
    path('dom-xss/', dom_xss, name='dom_xss'), # DOM-Based XSS
]
