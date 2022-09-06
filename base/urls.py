from django.urls import path
from . import views
from rest_framework_simplejwt.views import (  
    TokenRefreshView,
)




urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.apiOverview,name='api-overview' ),
    path('payment-list/',views.PaymentList,name='payment-list' ),
    path('payment-detail/<str:pk>/',views.PaymentDetail,name='payment-detail'),
    path('payment-create/',views.PaymentCreate,name='payment-create'),
    path('payment-update/<str:pk>/',views.PaymentUpdate,name='payment-update'),
    path('payment-delete/<str:pk>/',views.PaymentDelete,name='payment-delete'),
    path('login/', views.loginPage,name="login"),
    path('register/', views.registerPage,name="register"),
    path('logout/', views.logoutUser,name="logout"),
]

'''
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjU0MDUyMywiaWF0IjoxNjYyNDU0MTIzLCJqdGkiOiJmOWU2ZWY0ZjdmYWM0MDk4ODg2OTk3OTMwM2M4OWJjOCIsInVzZXJfaWQiOjF9.Pc2Ypsy-ViOudp1hZi5n9qM7d93xuTSi0xngCD9BaJU",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYyNDU0NDIzLCJpYXQiOjE2NjI0NTQxMjMsImp0aSI6ImU1ODliYjIxYzVkYzQwMGI4NWRiYjBiNzU1NjI3NGQ3IiwidXNlcl9pZCI6MX0.TwBKezrTik8Kvuae3Tl0rt2e6qmzSPLOmHP7Zd5r6t8"
}
'''

