from django.urls import path
from .views import RegisterView, MeView, LoginView, AdminDashboardDataView, PasswordUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("password/update/", PasswordUpdateView.as_view(), name="password_update"),
    path("admin/dashboard-data/", AdminDashboardDataView.as_view(), name="admin_dashboard_data"),

]
