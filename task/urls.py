from django.urls import path
from . import views


urlpatterns = [
	path('', views.tasks, name='homepage'),
	path('detail/<int:pk>', views.detail, name='task_detail'),
	path('sign_up/', views.sign_up, name='sign_up'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('add_task/', views.add_task, name='add_task'),
	path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
	path('delete_task/<int:pk>', views.delete_task, name='delete_task')
]