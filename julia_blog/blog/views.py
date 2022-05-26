from urllib import response
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post,Message
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from users.models import Profile
from PIL import Image
from django.urls import reverse
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Q
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# from extra_views import CreateWithInlinesView, InlineFormSet

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context["tags"] = Tag.objects.all() 
        return context

    def get_queryset(self):
        slug = self.request.GET.get('search')

        if slug:
            return Post.objects.filter(
                Q(tags__name__in=slug) |
                Q(title__icontains=slug) |
                Q(content__icontains=slug)
            ).order_by('-date_posted')

        
        return Post.objects.all().order_by('-date_posted')

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(TagPostListView, self).get_context_data(**kwargs)
        context["tags"] = Tag.objects.all() 
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug')).order_by('-date_posted')

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

    def get_context_data(self,**kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked

        return context
        
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            postid = request.POST.get('postid')
            comment = request.POS.get('comment')            
            # post = Post.objects.get(pk=postid)
            user = request.user
            Message.objects.create(
                user = user,
                post_id = postid,
                body = comment
            )
            return JsonResponse({'bool':True})

# def save_comment(request):
#     return JsonResponse({'bool':'true'})

    #     messages  = Message.objects.all(post_id=self.kwargs.get('pk'))
    #     context = { "topics":messages}

    #     return render(request,"blog/post_detail.html",context)

    # def post(self, request, *args, **kwargs):
    #     # json    = { "error":True }
    #     message = Message.objects.create(
    #         user=request.user,
    #         post_id=self.kwargs.get('pk'),
    #         body=request.POST.get('body')
    #         )
    #     message.save()



    #     # json["error"]   = False

    #     messages = Message.objects.filter(post_id=self.kwargs.get('pk'))
    #     context = { "messages":messages }
    #     # content = render_to_string("base.html",context,request)

    #     # json["content"] = content

        # return JsonResponse({'bool':'true'})
        
        # return redirect('post-detail', pk=self.kwargs.get('pk'))

# def post_detail_data(request):
#         # try:
            # # stuff = get_object_or_404(Post, id=self.kwargs['pk'])
            # total_likes = stuff.total_likes()
            
            # liked = False
            # if stuff.likes.filter(id=self.request.user.id).exists():
            #     liked = True
#         # except:
#         #     raise Http404

#         data = {
#             'total_likes':total_likes,
#             'liked':liked,
#             'messages':stuff.message_set.all(),
#         }
#         return JsonResponse(data)


# class ImagesInlineFormSet(InlineFormSet):
#     model = PostImage
#     fields = ("image", )
#     can_delete = False  No need to delete in create view


# class PersonCarCreateFormsetView(CreateWithInlinesView):
#     model = Person
#     fields = ("name", "age")  # self.model fields
#     inlines = [CarInlineFormSet, ]
#     template_name = "person_formset.html"
#     success_url = "/"

class PostCreateView(LoginRequiredMixin,CreateView):
# class PostCreateFormsetView(LoginRequiredMixin,CreateWithInlinesView):
    model = Post
    fields = ('title','content','tags','thumbnail','headerImage')
    # inlines = [ImagesInlineFormSet, ]

    def get_form(self, form_class=None):
        form = super(PostCreateView, self).get_form(form_class)
        # form = super(PostCreateFormsetView, self).get_form(form_class)
        form.fields['tags'].required = False
        return form

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','tags','thumbnail','headerImage']

    def get_form(self, form_class=None):
        form = super(PostUpdateView, self).get_form(form_class)
        form.fields['tags'].required = False
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

def LikeView(request,pk):
    # pk = request.POST.get('id')
    article = Post.objects.get(id=pk)
    
    total_likes = article.total_likes()  

    liked = True

    if article.likes.filter(id=request.user.id).exists():
        liked = False

    data = {
        'id': pk,
        'likes': total_likes,
        'is_liked':liked,
    }
    return JsonResponse(data)
