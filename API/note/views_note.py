''' 5. using ModelViewSet,the easist way to bulid Rest API in backend
(The ModelViewSet inherits from/pack GenericAPIView)

from .models import Posts
from .serializers import PostSerializer
from rest_framework import viewsets

# the class inculde all CRUD methods
class PostViewset(viewsets.ModelViewSet):

    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # overwrite the create method
    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     newThing = Post.objects.create(field=data["filed"],....)
    #     newThing.save()
    #     serializer = theSerializer(newThing)
    #     return Response(serializer.data)

    # overwrite the perform_create to automatically add the current user into "author" field
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
        postObject.description = data.get("description", postObject.description)
        postObject.cover = data.get("cover", postObject.cover)
        try:
            # don't have the field of username, this will be passed 
            author = User.objects.get(username=data["username"])
            postObject.author = author
        except KeyError:
            pass
        postObject.save()

        # add or remove user's likes into many-to-many field
        # check if current user has already liked this post 
        # if data["userlikes"] in postObject.userlikes.all(): 
        if postObject.userlikes.filter(username=data["userlikes"]).exists():
            postObject.userlikes.add(data["userlikes"])
        else:
            postObject.userlikes.remove(data["userlikes"])

        # send request context to get the absolute url of 'cover' image
        serializer = PostSerializer(postObject, context={"request": request})

        return Response(serializer.data)

    # # overwrite the partial update method (another way)
    def update(self, request, *args, **kwargs):
        postObject = self.get_object()
        data = request.data

        # change partial to True changing only provided fields
        serializer = self.get_serializer(
            postObject, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
'''


''' 4. using GenericViewSet and mixins, make coed concised 
(The GenericViewSet inherits from/pack GenericAPIView)

from .models import Posts
from .serializers import PostSerializer
from rest_framework import mixins
from rest_framework import viewsets

# the class inculde all CRUD methods
class PostViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = Posts.objects.all()
    serializer_class = PostSerializer

'''


''' 3. using viewsets and Router in urls.py, all CRUD methods can be contained in one viewsets class 
# (The ViewSet inherits from/pack APIView)

from .models import Posts
from .serializers import PostSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

# the class inculde all CRUD methods
class PostViewset(viewsets.ViewSet):

    def list(self, request):
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Posts.objects.all()
        thePost = get_object_or_404(queryset, pk=pk)
        # thePost = Posts.objects.get(pk=pk) # should handle the not found response
        serializer = PostSerializer(thePost)
        return Response(serializer.data)

    def update(self, request, pk=None):
        thePost = Posts.objects.get(pk=pk)
        serializer = PostSerializer(thePost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        thePost = Posts.objects.get(pk=pk)
        thePost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


''' 2. using GenericAPIView and mixins, make coed concised 
# (GenericAPIView inherits from/pack the APIView)

from .models import Posts
from .serializers import PostSerializer
from rest_framework import generics, mixins 

# the class to read and create (no post is specified)
class PostList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    # from GenericAPIView
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # from mixins
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# the class to get the detail or modify or delete the corresponding post
class PostDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    
    # from GenericAPIView
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # from mixins
    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)

#################################### or even more concise (without mixins)... ####################################
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
'''


''' 1.2. using class API 
# (APIView inherits from/pack View in Django)

from .models import Posts
from .serializers import PostSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

# the name of functions in calss have to be exactly get, post, put, delete

# the class to read and create (no post is specified)
class PostList(APIView):

    # read all data from database
    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # store new data into database
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# the class to get the detail or modify or delete the corresponding post
class PostDetail(APIView):

    def getThePost(self, pk):
        try:
            # get the corresponding data
            return Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            # not found
            return Response(status=status.HTTP_404_NOT_FOUND)

    # read the the corresponding data in database
    def get(self, request, pk):
        thePost = self.getThePost(pk)
        serializer = PostSerializer(thePost)
        return Response(serializer.data)

    # modify the corresponding data in database
    def put(self, request, pk):
        thePost = self.getThePost(pk)
        serializer = PostSerializer(thePost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # 400 means bad request error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete the corresponding data in database
    def delete(self, request, pk):
        thePost = self.getThePost(pk)
        thePost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


''' 1.1. using functional API 
# (api_view inherits from/pack View in Django)

from .models import Posts
from .serializers import PostSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status


# the function to read and create (no post is specified)
@api_view(['GET', 'POST'])
def PostList(request):

    # read all data from database
    if request.method == 'GET':
        # read all data from database
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # store new data into database
    elif request.method == 'POST':
        # store new data into database
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# the function to get the detail or modify or delete the corresponding post
@api_view(['GET', 'PUT', 'DELETE'])
def PostDetail(request, pk):
    try:
        # get the corresponding data
        thePost = Posts.objects.get(pk=pk)
    except Posts.DoesNotExist:
        # not found
        return Response(status=status.HTTP_404_NOT_FOUND)

    # read the the corresponding data in database
    if request.method == 'GET':
        serializer = PostSerializer(thePost)
        return Response(serializer.data)

    # modify the corresponding data in database
    elif request.method == 'PUT':
        # store modified data to the corresponding post in database
        serializer = PostSerializer(thePost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # 400 means bad request error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete the corresponding data in database
    elif request.method == 'DELETE':
        thePost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''


''' 0. using Django View without any rest framework
https://www.django-rest-framework.org/tutorial/1-serialization/
'''
