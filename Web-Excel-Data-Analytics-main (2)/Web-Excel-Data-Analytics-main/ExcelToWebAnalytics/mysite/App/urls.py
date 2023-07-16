from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>//sheet/<str:file_name>/<str:sheet_name>/', views.sheet, name='sheet'),
    path('file/<int:file_id>//sheet_columns/<str:file_name>/<str:sheet_name>/<str:col_name>/', views.sheet_columns,
         name='sheet_columns')

]
