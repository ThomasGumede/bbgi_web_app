from django.urls import path
from accounts.views.account_views import account_update, activate, activation_sent, add_social_links, confirm_email, custom_login, custom_logout, general, register, user_details
from accounts.views.password_views import password_change, password_reset_request, password_reset_sent, passwordResetConfirm
from accounts.views.subscribe_views import choose_package
app_name = "accounts"
urlpatterns = [
    path("login", custom_login, name="login"),
    path('logout', custom_logout, name='logout'),
    path("register", register, name="register"),
    path('details/<str:username>', user_details, name="user-details"),
    path('register/success', activation_sent, name='success'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('confirm/email/<uidb64>/<token>', confirm_email, name='confirm-email'),
    path("password/reset", password_reset_request, name="password-reset"),
    path('password/success', password_reset_sent, name='password-reset-sent'),
    path('password/reset/<uidb64>/<token>', passwordResetConfirm, name='password-reset-confirm'),
    path("password/reset", password_reset_request, name="password-reset"),
    path('password/success', password_reset_sent, name='password-reset-sent'),
    path('password/reset/<uidb64>/<token>', passwordResetConfirm, name='password-reset-confirm'),

    path('update/profile', account_update, name="profile-update"),
    path('update/contact', general, name="contact-update"),
    path('update/password', password_change, name="password-update"),
    path('update/social', add_social_links, name="update-social-links"),
    path('subscribe', choose_package, name="choose-package")
]
