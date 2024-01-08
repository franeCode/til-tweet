from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from followers.models import Follower
from django.contrib.auth.models import User

class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/homepage.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        posts = Post.objects.all().order_by('-id')[0:30]
        context['posts'] = posts
        return context


class PostDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = "/"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True
            },
            content_type="application/html"
        )
        
class ProfileView(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/detail.html"
    model = User 
    context_object_name = "user"
    
