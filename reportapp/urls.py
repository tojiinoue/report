from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "reportapp"

urlpatterns = [
    path('', views.index, name='top'),
    path('create/', views.ReportCreate.as_view(), name='report_create'),
    path('list/', views.ReportList.as_view(), name='report_list'),
    path('update/<int:pk>/', views.ReportUpdate.as_view(), name='report_update'),
    path('delete/<int:pk>/', views.ReportDelete.as_view(), name='report_delete'),
    path('like/<int:pk>/', views.like_report, name='report_like'),
    path('detail/<int:pk>/', views.ReportDetail.as_view(), name='report_detail'),
    path('commnet/<int:pk>/', views.comment_report, name='report_comment'),
    path('userlist/', views.UserList.as_view(), name='user_list'),
    path('userReport/<int:pk>/', views.UserReportList.as_view(), name='user_report_list'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]