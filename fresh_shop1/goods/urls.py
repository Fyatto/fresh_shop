from django.urls import path

from goods import views

urlpatterns = [
    # 首页
    path('index/', views.index, name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),
    # 最近浏览记录
    path('recent_browse/', views.recent_browse, name='recent_browse'),
    path('goods_list/<int:id>/', views.goods_list, name='goods_list'),
]