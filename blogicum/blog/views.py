from django.contrib.auth import get_user_model, login, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post
from .service import get_published_posts, paginate_queryset

User = get_user_model()


def index(request):
    """Главная страница блога: список постов в обратном порядке."""
    posts = get_published_posts()
    page_obj = paginate_queryset(posts, request)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Детальная страница поста."""
    post = get_object_or_404(
        Post.objects
        .select_related('author', 'category', 'location'),
        id=post_id,
    )

    now = timezone.now()
    can_edit = request.user.is_authenticated and request.user == post.author
    is_public = (
        post.is_published
        and post.pub_date <= now
        and post.category.is_published
    )
    if not can_edit and not is_public:
        raise Http404('Запрашиваемый пост отсутствует')

    comments = post.comments.all().select_related('author')
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории: отображает посты указанной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = (
        get_published_posts(category.posts.all())
    )
    page_obj = paginate_queryset(posts, request)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


@login_required
def create_post(request):
    """Страница добавления публикации."""
    form = PostForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


def profile_view(request, username):
    """Страница пользователя."""
    user = get_object_or_404(User, username=username)
    is_owner = request.user.is_authenticated and request.user == user
    posts = get_published_posts(
        queryset=user.posts.all(),
        need_filter=not is_owner,
    )

    page_obj = paginate_queryset(posts, request)

    context = {
        'profile': user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class LoginView(auth_views.LoginView):
    """Кастомизированное представление для входа пользователя."""

    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


@login_required
def edit_profile_view(request):
    """Страница редактирования профиля."""
    form = ProfileForm(
        request.POST or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect(
            'blog:profile',
            username=request.user.username,
        )
    return render(
        request,
        'blog/edit_profile.html',
        {'form': form},
    )


class RegistrationView(CreateView):
    """Представление регистрации пользователя."""

    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username},
        )


@login_required
def add_comment(request, post_id):
    """Страница для добавления комментария."""
    post = get_object_or_404(Post, pk=post_id)

    if request.method != 'POST':
        return redirect('blog:post_detail', post_id=post_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(
        request,
        'blog/detail.html',
        {'post': post, 'comments': post.comments.all(), 'form': form},
    )


@login_required
def edit_post(request, pk):
    """Страница редактирования публикации."""
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.pk)

    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.pk)
    context = {
        'form': form,
    }
    return render(request, 'blog/create.html', context)


@login_required
def edit_comment(request, post_id, comment_id):
    """Страница редактирования комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(
        request,
        'blog/comment.html',
        {
            'form': form,
            'comment': comment,
        },
    )


@login_required
def delete_post(request, pk):
    """Удаление публикации."""
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    # GET — показываем подтверждающую страницу
    context = {
        'form': PostForm(instance=post),
    }
    return render(request, 'blog/create.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)
