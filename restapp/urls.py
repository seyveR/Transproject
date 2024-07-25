from django.urls import path
from .views import StartPageView, PriemkaView, PreProcessView, SaveDataView, ReportView
from . import views

urlpatterns = [
    path('', StartPageView.as_view(), name='startpage'),
    path('priemka/', PriemkaView.as_view(), name='priemka'),
    path('priemka/pre_process/', PreProcessView.as_view(), name='pre_process'),
    path('priemka/pre_process/savedata/', SaveDataView.as_view(), name='savedata'),
    path('report/', ReportView.as_view(), name='report'),
    path('auth/', views.auth, name='auth'),
    path('logout', views.logout_user, name='logout'),
]