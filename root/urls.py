from django.urls import path
from . import views


urlpatterns = [
    path('model/', views.Model_view.as_view(), name='modelView'),
    path('json/<int:id>/', views.Model_Json_Download.as_view(), name='json')
]
