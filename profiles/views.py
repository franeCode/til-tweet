from typing import Any
from django.contrib.auth.models import User
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse 
from django.views.generic import DetailView, View, UpdateView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from django.contrib import messages
from .models import Profile
from django.urls import reverse_lazy


class ProfileDetailView(DetailView):
    html_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User 
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        
        context['user_posts'] = Post.objects.filter(author=user).order_by('-id')[0:30]
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_following'] = Follower.objects.filter(following=user).count()
        context['total_followed_by'] = Follower.objects.filter(followed_by=user).count()
        
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if data['action'] == "follow":
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user
                )
            except Follower.DoesNotExist:
                follower = None
                
            if follower:
                follower.delete()
                
        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "follow" else "Follow"
        })

class EditProfileView(LoginRequiredMixin, UpdateView):
    http_method_names = ["post"]
    template_name = "profiles/detail.html"
    model = Profile 
    context_object_name = "user"
    slug_field = "user__username"
    slug_url_kwarg = "username"
    fields = ['name', 'image', 'bio', 'cover', 'coding_stack']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].initial = self.object.name
        form.fields['bio'].initial = self.object.bio
        form.fields['coding_stack'].initial = self.object.coding_stack.all()
        return form

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Your profile was updated successfully')
        self.object = form.save()
        return JsonResponse({'success': True, 'redirect_url': reverse_lazy('profiles:detail', kwargs={'username': self.object.user.username})})

    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'username': self.object.user.username})