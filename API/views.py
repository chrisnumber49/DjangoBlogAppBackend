from rest_framework.response import Response
from .models import Posts, Comments
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from rest_framework import status
# Create your views here.


# the viewset class inculde all CRUD methods
class PostViewset(viewsets.ModelViewSet):

    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    # adding required permissions to this views to restrict unauthenticated user
    permission_classes = [IsAuthenticatedOrReadOnly]
    # for the authentication, can access only when you request with token
    authentication_classes = (TokenAuthentication,)
    # for the searching
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'author__username']

    # overwrite the create method to automatically add the current user into "author" field
    def perform_create(self, serializer):
        # get the user id with token
        # user_id = Token.objects.get(key=self.request.auth.key).user_id
        # get user name with user id
        # user = User.objects.get(id=user_id).username
        # fill user name into the author field to show which user posted/edited it
        serializer.save(author=self.request.user)

    # overwrite the partial update method (one way)
    def partial_update(self, request, *args, **kwargs):
        postObject = self.get_object()
        data = request.data

        # use new data if there is data from title field in front, otherwise use the old data
        postObject.title = data.get("title", postObject.title)
        postObject.description = data.get(
            "description", postObject.description)
        postObject.cover = data.get("cover", postObject.cover)
        try:
            author = User.objects.get(username=data["username"])
            postObject.author = author
        except KeyError:
            pass
        postObject.save()

        # send request context to get the absolute url of 'cover' image
        serializer = PostSerializer(postObject, context={"request": request})

        return Response(serializer.data)

    # # overwrite the partial update method (another way)
    # def update(self, request, *args, **kwargs):
    #     postObject = self.get_object()
    #     data = request.data

    #     # change partial to True changing only provided fields
    #     serializer = self.get_serializer(
    #         postObject, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data)


# the viewset class for users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

# the viewset class for comments


class CommentViewset(viewsets.ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # adding required permissions to this views to restrict unauthenticated user
    permission_classes = [IsAuthenticatedOrReadOnly]
    # for the authentication, can access only when you request with token
    authentication_classes = (TokenAuthentication,)

    # overwrite the create method to automatically add the current user into "author" field
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
