from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog, Comment
from .forms import BlogForm
from django.core.paginator import Paginator
from .forms import CommentForm
# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-pub_date')
    query = request.GET.get('query')
    if query:
        blogs = Blog.objects.filter(title__contains=query)
    
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    paginated_blogs = paginator.get_page(page)
    return render(request, 'home.html',{'blogs':paginated_blogs})

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post_id = id).order_by('-created_time')
    return render(request, 'detail.html', {"blog" : blog, "comment_form":comment_form, "comments":comments})


def new(request):
    return render(request, 'new.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    new_blog.body = request.POST['body']
    new_blog.image = request.FILES['image']
    new_blog.pub_date = timezone.now()
    new_blog.save()
    return redirect('blog:detail', new_blog.id)

def update(request, id):
    blog = Blog.objects.get(id = id)
    if request.method == "POST":
        blog.title = request.POST["title"]
        blog.body = request.POST["body"]
        blog.save()
        return redirect('blog:detail', blog.id)
    return render(request, 'update.html', {"blog" : blog})

def delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("home")

def new_with_django_form(request):
    form = BlogForm()
    return render(request, 'new_with_django_form.html', {'form':form})

def create_with_django_form(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        if request.user.is_authenticated:
            new_blog.user = request.user
        new_blog.save()
        return redirect('blog:detail', new_blog.id)
    return redirect('home')

def comments_create(request, id):
  form = CommentForm(request.POST)
  if form.is_valid():
    create_form = form.save(commit=False)
    create_form.post = get_object_or_404(Blog, pk=id)
    if request.user.is_authenticated:
      create_form.user = request.user
    create_form.save()
  return redirect('blog:detail', id)

def comments_delete(request, blog_id, comment_id):
  comment = Comment.objects.get(pk = comment_id)
  if request.user.is_authenticated:
    comment.delete()
  return redirect('blog:detail', blog_id)
