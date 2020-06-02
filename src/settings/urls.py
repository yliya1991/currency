from django.contrib import admin
from django.urls import path, include # noqa
from django.views.generic import TemplateView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('rate/', include('rate.urls_rate')),

    path('account/', include('account.urls')),
]
