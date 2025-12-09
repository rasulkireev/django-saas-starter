from django.urls import path

from apps.blog import views

urlpatterns = [
    path("", views.BlogView.as_view(), name="blog_posts"),
    path("<slug:slug>", views.BlogPostView.as_view(), name="blog_post"),
]
