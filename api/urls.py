from django.urls import path

from .views import ItemsViewOne, ItemsViewTwo

urlpatterns = [
    path('items/', ItemsViewOne.as_view()),
    path('items-two/', ItemsViewTwo.as_view())
]