from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .import views

from .views import *
urlpatterns=[
path('my/',my),
path('login/',login_page),
path('logout/',logout_page),
path('boxAction/',boxActionIView.as_view()),
path('filter/',filter),
path('my_filter/',my_filter),
path('delete/<int:pk>/',views.delete),
path('update/',views.put),
]