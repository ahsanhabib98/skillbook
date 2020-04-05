from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from skillbook_app.forms import PostForm
from skillbook_app.models import Post, PostCategory
from users.models import Profile


class PostCreatView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_message = 'Successfully created your new post.'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'
    success_message = 'Successfully updated your post.'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.get_object().category.pk
        return context


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_message = 'Successfully deleted your post.'
    success_url = reverse_lazy('home')


class PostCategoryView(DetailView):
    model = PostCategory
    context_object_name = 'category'
    template_name = 'posts/post_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = PostCategory.objects.exclude(pk=self.kwargs['pk'])
        return context


@login_required
def add_to_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.liked.add(request.user.profile)
    post.save()
    messages.info(request, "You liked a new post.")
    return redirect('home')


@login_required
def remove_from_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.liked.remove(request.user.profile)
    messages.info(request, "Remove your like.")
    return redirect('home')
