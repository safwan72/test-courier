from django.urls import path
from . import views
app_name='App_Login'
urlpatterns = [
path('', views.HomeView.as_view(),name='home'),
path('signup/', views.signupview,name='signup'),
path('login/', views.login_view,name='login'),
path('profile_update/', views.merchant_profile_change,name='profile_update'),
path('logout/', views.logout_view,name='logout'),
]
