from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Post
from .constants import POSTS_PER_PAGE


def get_published_posts(queryset=None, *, need_filter=True, need_count=True):
    """Возвращает QuerySet постов с опциональной фильтрацией и подсчётом."""
    queryset = queryset or Post.objects
    queryset = queryset.select_related('author', 'category', 'location')
    if need_count:
        queryset = queryset.annotate(comment_count=Count('comments'))
    if need_filter:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    return queryset.order_by('-pub_date')


def paginate_queryset(queryset, request, page_size=POSTS_PER_PAGE):
    """Пагинирует queryset на основе GET-параметра 'page' из request."""
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(page_number)
