from django.urls import path
from .views import*

urlpatterns = [
    path('',index,name="index"),
    path('globalnews/',globalNews,name="globalnews"),
    path('readadminnews/<nid>',readadminnews,name="readadminnews")
]