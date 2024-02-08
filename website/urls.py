from django.urls import path, include, re_path
from website.views import Homepage,Logout_user,Register_User,CustomerRecord,Api,UpdateRecord,DeleteRecord,AddRecord

urlpatterns = [
    path('record/<int:pk>/',CustomerRecord.as_view(),name='Cust_record'),
    path('',Homepage.as_view(),name='homepage'),
    path('register/',Register_User.as_view(),name='register'),
    path('logout/',Logout_user.as_view(),name='logout'),
    path('add/',AddRecord.as_view(), name="addrecord"),
    re_path(r'api/(endpoints|\d+)/',Api.as_view(),name='apiurl'),
    path('api/delete/<int:pk>/',DeleteRecord.as_view(),name='delete'),
    path('api/delete/',DeleteRecord.as_view(),name='delete'),
    path('api/update/<int:pk>/',UpdateRecord.as_view(),name='update'),
    path('api/update/',UpdateRecord.as_view(),name='update'),
    path('api/add/', AddRecord.as_view(), name="addrecord")
]