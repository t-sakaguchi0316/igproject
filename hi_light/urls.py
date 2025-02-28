#hi_light/urls
from django.urls import path
from . import views
from .views import NotificationListView


app_name = 'hi_light'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('discover/', views.DiscoverView.as_view(), name='discover'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('post/', views.CreatePhotoView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/edit/done/', views.EditSuccessView.as_view(), name='edit_done'),
    path('detail/', views.DetailView.as_view(), name='detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('liked_posts/', views.liked_posts, name='liked_posts'),
    
]

urlpatterns += [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]


