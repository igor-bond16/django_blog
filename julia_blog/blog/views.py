from urllib import response
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post,Topic,Message
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from users.models import Profile
from PIL import Image


# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context["topics"] = Topic.objects.all() 
        return context

    def get_queryset(self):
        q_param = self.request.GET.get('q')

        if q_param:
            return Post.objects.filter(topic__name__icontains=q_param).order_by('-date_posted')

        return Post.objects.all().order_by('-date_posted')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context["profile"] = Profile.objects.filter(user__username=self.kwargs.get("username")).first()
        return context

class PostDetailView(DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        message = Message.objects.create(
            user=request.user,
            post_id=self.kwargs.get('pk'),
            body=request.POST.get('body')
            )
        message.save()
        
        return redirect('post-detail', pk=self.kwargs.get('pk'))


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','topic','thumbnail']

    def get_form(self, form_class=None):
        form = super(PostCreateView, self).get_form(form_class)
        form.fields['topic'].required = False
        return form

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','topic','thumbnail']

    def get_form(self, form_class=None):
        form = super(PostUpdateView, self).get_form(form_class)
        form.fields['topic'].required = False
        return form

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False