from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.quiz_view, name='quiz'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('logout/', views.logout_view, name='logout'),

]
