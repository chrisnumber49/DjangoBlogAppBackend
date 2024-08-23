from rest_framework import serializers
from .models import Posts, Comments
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token

# serializers is for the data conversion to serialize and generate the json or xml format


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comments
        fields = ['id', 'post', 'author', 'body']


class PostSerializer(serializers.ModelSerializer):
    # related_name="comments" in the Comments Model (Nested relationships)
    postComments = CommentSerializer(many=True, read_only=True)
    # to show the specific detail of ForeignKey User (method 2)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Posts
        fields = ['id', 'title', 'description',
                  'cover', 'author', 'postComments']
        # to show all the detail of ForeignKey User (method 1)
        # depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # will only show username in page
        # fields = '__all__'

        # this will make password invisible
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    # overwirte the creat method to let the password of new user be hashing password (valid format)
    def create(self, validated_data):
        newUser = User.objects.create_user(**validated_data)
        # create a token for the new user who resgiter
        Token.objects.create(user=newUser)
        return newUser
