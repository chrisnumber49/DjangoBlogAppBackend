from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# for uploading and showing the image
from django.conf.urls.static import static
from django.conf import settings

# when using viewsets we need to register the router
router = DefaultRouter()
router.register('posts', views.PostViewset, basename='posts')
router.register('users', views.UserViewSet)
router.register('comments', views.CommentViewset)

urlpatterns = [
    path('api/', include(router.urls)),
]


# for uploading and showing the image
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

''' 1.2 using class API
urlpatterns = [
    path('posts/', views.PostList.as_view(), name='posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='thePost'),
]
'''

''' 1.1 using functional API
urlpatterns = [
    path('posts/', views.PostList, name='posts'),
    path('posts/<int:pk>/', views.PostDetail, name='thePost'),
]
'''
