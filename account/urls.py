from django.urls import path
from .views import LandlordSignUpView, signup, AgencySignUpView, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("signup/agency", AgencySignUpView.as_view(), name="agency-signup"),
    path("signup/landlord", LandlordSignUpView.as_view(), name="landlord-signup"),

    # authentication
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # password change  
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    # reset password
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")

]
