
from django.conf.urls import url  
from django.contrib import admin
from django.urls import path
from community import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [  
    path('login/', views.login.as_view(), name='login'),
    path('chage_success/', views.change_success.as_view(), name='change_success'),
    path('signup_st/', views.signup_st.as_view(), name='signup_st'),
    path('signup_pf/', views.signup_pf.as_view(), name='signup_pf'),
    path('signup_select/', views.signup_select.as_view(), name='signup_select'),
    path('change/', views.change.as_view(), name='change'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('board/', views.IndexView.as_view(), name='board'),
    path('board/<int:identifier>/', views.BoardCa.as_view(), name='board_category'),
    path('board/<int:identifier>/<int:identifier2>', views.BoardCons.as_view(), name='board_con'),
    path('board/<int:identifier>/<int:identifier2>/post_write/', views.PostWrite.as_view(), name='post_write'),
    path('board/<int:identifier>/<int:identifier2>/<int:identifier3>/', views.BoardMessage.as_view(), name='board_message'),
    path('board/<int:identifier>/<int:identifier2>/<int:identifier3>/post_modify/', views.PostModify.as_view(), name='post_modify'),
    #path('success_post/', views.TemplateView.as_view(template_name='board/success_post.html'), name='success_post'),
    path('', views.main.as_view(), name='main'),
]