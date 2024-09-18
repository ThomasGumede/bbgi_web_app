from django.urls import path
from accounts.views.company import update_company_address
from accounts.views.account_views import account_update, activate, activation_sent, add_social_links, confirm_email, custom_login, custom_logout, general, register, user_details
from accounts.views.password_views import password_change, password_reset_request, password_reset_sent, passwordResetConfirm
from accounts.views.subscribe_views import cancel_subscription_order, choose_package, subscribe, subscription_checkout
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

    path('dashboard/update/profile', account_update, name="profile-update"),
    path('dashboard/update/contact', general, name="contact-update"),
    path('dashboard/update/password', password_change, name="password-update"),
    path('dashboard/update/social', add_social_links, name="update-social-links"),

    path('dashboard/update/company-details', update_company_address, name="update-company-details"),
    path('subscribe', choose_package, name="choose-package"),
    path('subscribe/<uuid:package_id>', subscribe, name="subscribe"),
    path('subscribe/checkout/<uuid:order_id>', subscription_checkout, name="subscription-checkout"),
    path('subscribe/cancel/<uuid:subscription_order_id>', cancel_subscription_order, name="cancel-subscription-order")
]
