from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Like
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


#def home(request):
#    context ={
#        'posts': Post.objects.all()
#    }
#
#   return render(request, 'blogapp/index.html', context)

def search(request):
    query = request.GET.get('q',"")
    if query:
        posts  = Post.objects.filter(Q(title__contains=query)|Q(author__username__contains=query))
    else:
        posts =[]
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'posts':posts, 'page_obj':page_obj,'query' : query,}
    return render(request, 'blogapp/search.html', context )


def validate_username(request):
    username = request.GET.get('username', '')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


class PostList(ListView):
    model = Post
    template_name = 'blogapp/index.html'
    context_object_name ='posts'
    ordering = ['-date_posted']
    paginate_by = 3
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         return context


class UserList(ListView):
    model = Post
    template_name = 'blogapp/user_posts.html'
    context_object_name ='posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetail(DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blogapp/about.html',)

def like(request):
    post = Post.objects.get(id=int(request.GET['post_id']))
    has_liked = Like.objects.filter(for_post=post, like_by=request.user)

    if  has_liked:
        has_liked.delete()
    else:
        liked =Like(for_post=post, like_by=request.user)
        liked.save()
    data = {
            'like_count':Like.objects.filter(for_post=post).count(),
        }
    return JsonResponse(data)

def coment(request):
    msg = request.GET.get('msg','')
    post= Post.objects.get(id=request.GET['post_id'])
    user = request.user
    new_coment = Comment(for_post=post, comment_by=user, msg=msg)
    new_coment.save()
    data ={
        'msg': new_coment.msg,
    }
    return JsonResponse(data)