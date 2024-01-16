from typing import Any
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from followers.models import Follower
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.template.loader import render_to_string

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
    
    def post_comment(request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        context = super().get_context_data(*args, **kwargs)
        comments = Comment.objects.filter(post=post).order_by('-id')
        context['comments'] = comments
        return context
    
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
        
class CommentView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id)
            comments_json = serialize('json', comments)
            return JsonResponse({'success': True, 'comments': comments_json})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
class CreateCommentView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, post_id, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=post_id).order_by('-id')
        return context
        
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comment_text = request.POST.get('comment_text')

        if comment_text:
            comment = Comment.objects.create(
                text=comment_text,
                author=request.user,
                post=post
            )

            return JsonResponse({
                'success': True,
                'comment_text': comment.text,
                'author': comment.author.username,
            })

        return JsonResponse({'success': False, 'errors': 'Comment text cannot be empty'})