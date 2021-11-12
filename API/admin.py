from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from .models import Posts, Comments
# Register your models here.

# the first way for data base admin (not detailed)
# dmin.site.register(Posts)


# the second way for data base admin (detailed)
@admin.register(Posts)
class PostModel(admin.ModelAdmin):
    list_filter = ('title', 'description')
    list_display = ('id', 'title', 'description', 'author')


@admin.register(Comments)
class CommentModel(admin.ModelAdmin):
    list_display = ('post', 'author', 'body')
