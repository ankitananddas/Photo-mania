from django.urls import path

from . import views
urlpatterns = [
    path('', views.Home, name='home'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:id>', views.profile, name="profile"),
    path('addpost/', views.add_post, name='add-post'),
    path('like/<int:id>', views.like, name='like'),
    path('search/', views.search, name="search"),
    path('follow/<int:id>/<str:username>/', views.follow, name="follow"),
]
