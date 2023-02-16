
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from users import views as userViews
from django.contrib.auth import views as authViews
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('reg/', userViews.register, name = 'reg'),
    path('delivery/', include ('delivery.urls')),
    path('users/', authViews.LoginView.as_view(template_name= 'users/users.html'), name = 'users'),
    path('exit/', authViews.LogoutView.as_view(template_name= 'users/exit.html'), name = 'exit'),
    path('profile/', userViews.profile, name = 'profile'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('payments/', include('payments.urls')),
]


urlpatterns += i18n_patterns (
    path('', include('main.urls')),
    path('reg/', userViews.register, name = 'reg'),
    path('delivery/', include ('delivery.urls')),
    path('users/', authViews.LoginView.as_view(template_name= 'users/users.html'), name = 'users'),
    path('exit/', authViews.LogoutView.as_view(template_name= 'users/exit.html'), name = 'exit'),
    path('profile/', userViews.profile, name = 'profile'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
