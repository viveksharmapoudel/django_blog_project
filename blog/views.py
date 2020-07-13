from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
        ListView,DetailView,
        CreateView, UpdateView, DeleteView
        )
from django.core.paginator import Paginator
from blog.models import * 



def home(request):
    context={
        'posts':Post.objects.all(),
    }
    return render(request,'blog/home.html', context)


###CRUD for the post view 
class PostListView(ListView):
    model=Post                      # this is default
    template_name='blog/home.html'  #<app>/<model>_<viewtype>.html 
    context_object_name='posts'
    ordering= ["-date_posted"]
    paginate_by=5 


class PostDetailView(DetailView):
    model = Post
    #template_name = ".html"


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields=['title','content']

    def form_valid(self , form): 
        form.instance.author= self.request.user
        return super().form_valid(form)


class PostUpdateView( LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields=['title','content']

    def form_valid(self , form): 
        form.instance.author= self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user== post.author: 
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url= reverse_lazy('blog-home')

    def test_func(self):
        post=self.get_object()
        if self.request.user== post.author: 
            return True
        return False


#user filter post list 
class UserPostListView(ListView):
    model=Post                      # this is default
    template_name='blog/user_posts.html'  #<app>/<model>_<viewtype>.html 
    context_object_name='posts'
    ordering= ["-date_posted"]
    paginate_by=5 

    def get_queryset(self):
        user=get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    

def about(request):
    return render(request,'blog/about.html')


