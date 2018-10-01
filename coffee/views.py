from django.shortcuts import redirect, render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect

from django.views import View

from .models import Post, Comment

from .forms import (
            CommentForm,
            RegistrationForm,
            PostForm
        )

# Create your views here.


class Home(View):
    def get(self, request, *args, **kwargs):
        home = Post.objects.all()
        post = home
        paginator = Paginator(home, 3)
        page = request.GET.get('page')
        try:
            home = paginator.page(page)
        except PageNotAnInteger:
            home = paginator.page(1)
        except EmptyPage:
            home = paginator.page(paginator.num_pages)
        context = {
            'home': home,
            'post': post,
        }
        return render(request, 'coffee/home.html', context)

class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post_detail = get_object_or_404(Post, slug = slug)
        post_list = Post.objects.all()
        comment_list = Comment.objects.all()
        paginator = Paginator(post_list, 5)
        page = request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        context = {
            'post': post_detail,
            'list': post_list,
            'comment': comment_list
        }
        return render(request, 'coffee/post_detail.html', context)

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostForm
    initial = {'key': 'value'}
    template_name = 'coffee/post_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('coffee:post-detail', slug = post.slug)
        else:
            form = PostForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def post_edit(request, slug):
    post_user = Post.objects.filter(user=request.user)
    post = get_object_or_404(post_user, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('coffee:post-detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'coffee/post_edit.html', context)

class CommentView(View):
    form_class = CommentForm
    initial = {'key': 'value'}
    template_name = 'coffee/comment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('coffee:post-detail', slug = post.slug)
        else:
            form = CommentForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

class RegisterFormView(View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        user_form = self.form_class(initial=self.initial)
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('coffee:home')
        else:
            form = RegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)