from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import include, path
from django.views.generic import TemplateView


from settings import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('rate/', include('rate.urls_rate')),

    path('account/', include('account.urls')),

    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password-reset.html'), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password-reset-conf.html'), name='password_reset_confirm'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
         template_name='registration/password-reset-done.html'), name='password_reset_done'),

    path('password_change/<int:pk>/', views.ChangePassword.as_view(), name='password_change'),

]

handler404 = views.handler404
handler500 = views.handler500
