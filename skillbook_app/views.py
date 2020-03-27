from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView

from skillbook_app.forms import PostForm
from skillbook_app.models import Post, PostCategory
from users.models import Profile


class PostCreatView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_message = 'Successfully created your new post.'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)


class PostCategoryView(DetailView):
    model = PostCategory
    context_object_name = 'category'
    template_name = 'posts/post_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = PostCategory.objects.exclude(pk=self.kwargs['pk'])
        return context


def add_to_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.liked.add(request.user.profile)
    post.save()
    messages.info(request, "You liked a new post.")
    return redirect('home')


def remove_from_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.liked.remove(request.user.profile)
    messages.info(request, "Remove your like.")
    return redirect('home')
