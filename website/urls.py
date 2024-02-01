from django.urls import path
from website.views import Homepage,Logout_user,Register_User
urlpatterns = [
    path('',Homepage.as_view(),name='homepage'),
    path('register/',Register_User.as_view(),name='register'),
    path('logout/',Logout_user.as_view(),name='logout'),
]