from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from blog import views as blog_views
from blog.views import RegistrationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', blog_views.LoginView.as_view(), name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationView.as_view(),
        name='registration'
    ),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler404 = 'pages.views.custom_404'
handler403 = 'pages.views.custom_403'
handler500 = 'pages.views.custom_500'
