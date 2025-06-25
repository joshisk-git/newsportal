from multiprocessing import context
from django.shortcuts import render

from newspaper.models import Advertisement, Post
from django.views.generic import ListView

from django.utils import timezone
from datetime import timedelta

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = "newsportal/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull = False, status="active"
    ).order_by("-published_at")[:4]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull = False, status="active"
            ).order_by("-published_at")[:5]
        
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago #gte = greater than or equal to
        ).order_by("-published_at")[:5]

        context["breaking_news"] = Post.objects.filter(
            published_at__isnull=False, status="active", is_breaking_news=True
        ).order_by("-published_at")[:3]

        
        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )
        
        return context
    
class  PostListView(ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1


    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    

        context["popular_posts"] = Post.objects.filter(
                published_at__isnull = False, status="active"
                ).order_by("-published_at")[:5]

            
        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
            )
        
        return context