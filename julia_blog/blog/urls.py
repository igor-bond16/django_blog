from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostUpdateView,PostDeleteView,UserPostListView,LikeView,TagPostListView,PostCreateView


urlpatterns = [
    path('',PostListView.as_view(),name='blog-home'),
    path('tag/<str:slug>',TagPostListView.as_view(),name='tagged-home'),
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>',PostDetailView.as_view(),name='post-detail'),
    # path('save-comment/',save_comment,name='save-comment'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    # path('post/new/',PostCreateFormsetView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('like/<int:pk>', LikeView, name='like_post'),
]