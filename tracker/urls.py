from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('search_tasks/', views.search_tasks, name='search_tasks'),
    path('daily/', views.daily_tasks, name='daily_tasks'),
    path('finance/', views.finance_tracker, name='finance'),

]