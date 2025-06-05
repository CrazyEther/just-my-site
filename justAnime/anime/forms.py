from django import forms
from .models import Comment, Anime

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }

class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ['title', 'description', 'image', 'year', 'genres', 'slug', 'episodes_count']
