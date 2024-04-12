from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post
from .form import PostForm



def post_list(request):
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES aquí
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('detalle_post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/crear_post.html', {'form': form})



def search_results(request):
    query = request.GET.get('q')
    # Realizar la búsqueda en los datos relevantes (por ejemplo, en los títulos o contenido de los posts)
    posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(text__icontains=query)
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})



def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return redirect('post_detail', pk=pk)