from django.views.generic import ListView

from skillbook_app.models import Post, PostCategory
from users.models import Profile


class Home(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = PostCategory.objects.all()
        context['curators_list'] = Profile.objects.all()
        return context
