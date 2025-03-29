from django.urls import path
from .views import user_list, basic_create, basic_delete, update_user, basic_load_task1

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('basic_create/', basic_create, name='token_refresh'),
    path('users/update/<int:pk>/', update_user, name='update-user'),
    path('basic_delete/<int:pk>/', basic_delete, name='token_refresh'),
    path('basic_loan_task1/', basic_load_task1, name='token_refresh'),

]

