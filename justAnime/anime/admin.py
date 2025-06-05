from django.contrib import admin
from .models import Anime, Genre, Comment

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'episodes_count')
    filter_horizontal = ('genres',)  # Вот тут, пиздец важная штука!

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('anime', 'user', 'created_at', 'text')
    search_fields = ('anime__title', 'user__username', 'text')
    list_filter = ('anime', 'user')


# Register your models here.
