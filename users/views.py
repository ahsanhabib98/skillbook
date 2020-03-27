from django.contrib.auth import authenticate, login
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, ListView

from skillbook_app.models import Post, PostCategory
from .forms import UserCreationForm, ProfileForm
from .models import Profile, UserProfile


class SignInView(View):
    def get(self, *args, **kwargs):
        template = 'users/signin.html'
        return render(self.request, template)

    def post(self, *args, **kwargs):
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.info(self.request, "Welcome {}.".format(user.name))
                return redirect('home')
        else:
            messages.warning(self.request, "Your email or password is not correct.")
            return redirect('users:signin')


class SignUpView(View):
    def get(self, *args, **kwargs):
        context = {
            'form': UserCreationForm
        }
        template = 'users/signup.html'
        return render(self.request, template, context)

    def post(self, *args, **kwargs):
        form = UserCreationForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(
                user=user,
                name=user.name,
                email=user.email
            )
            login(self.request, user)
            messages.info(self.request, "Welcome {}.".format(user.name))
            return redirect('home')
        messages.warning(self.request, "Your password does not matching or account already exist.")
        return redirect('users:signup')


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile.html'


class EditProfileView(View):
    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        form = ProfileForm(instance=profile)
        context = {
            'form': form
        }
        template = 'users/edit_profile.html'
        return render(self.request, template, context)

    def post(self, *args, **kwargs):
        form = ProfileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            user = self.request.user
            if user.email != profile.email:
                if UserProfile.objects.filter(email=profile.email).exists():
                    messages.warning(self.request, "Your can not use this email cz this account already exist.")
                    return redirect('users:edit-profile')

            userProfile = Profile.objects.get(user=user)
            userProfile.name = profile.name
            user.name = profile.name
            userProfile.email = profile.email
            user.email = profile.email
            userProfile.designation = profile.designation
            userProfile.bio = profile.bio
            userProfile.source_bio = profile.source_bio
            userProfile.save()
            user.save()
            messages.info(self.request, "Updated your profile.")
            return redirect('home')
        messages.info(self.request, "Your profile data is not valid.")
        return redirect('users:edit-profile')


class ProfileListView(ListView):
    model = Profile
    context_object_name = 'curators_list'
    template_name = 'users/curators_list.html'


class ProfileWiseLikedPostView(ListView):
    model = Post
    context_object_name = 'liked_post_list'
    template_name = 'posts/liked_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = PostCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = self.request.user.profile.liked_posts.all()
        return queryset
