from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm

from .models import Anime, Genre, UserAnimeProgress, Comment
from .forms import CommentForm, AnimeForm

def anime_list(request):

    animes = Anime.objects.all()

    genre = request.GET.get('genre')
    year = request.GET.get('year')
    title = request.GET.get('title')

    if genre:
        animes = animes.filter(genres__name__iexact=genre)
    if year:
        animes = animes.filter(year=year)
    if title:
        animes = animes.filter(title__icontains=title)

    all_genres = Genre.objects.all()
    years = Anime.objects.order_by('-year').values_list('year', flat=True).distinct()

    return render(request, 'anime/anime_list.html', { 'animes': animes, 'all_tags': all_genres, 'available_years': years } )

@login_required
def update_progress(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    user = request.user

    # Найдём или создадим запись о прогрессе
    progress, created = UserAnimeProgress.objects.get_or_create(user=user, anime=anime)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'start':
            print("ACTION:", action)
            progress.watched_episodes = 0
            progress.status = 'watching'
            progress.save()
        elif action == 'add_one':
            if progress.watched_episodes < anime.episodes_count:
                progress.watched_episodes += 1
                progress.save()
        elif action == 'set_episode':
            try:
                episode = int(request.POST.get('set_episode'))
                if 0 <= episode <= anime.episodes_count:
                    progress.watched_episodes = episode
                    progress.save()
            except (ValueError, TypeError):
                pass  # Игнорируем мусор
        return redirect('anime_detail', slug=anime.slug)

    return redirect('anime_detail', slug=anime.slug)

def anime_detail(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    progress = None
    comments = anime.comments.select_related('user').order_by('-created_at')
    if request.user.is_authenticated:
        progress = UserAnimeProgress.objects.filter(user=request.user, anime=anime).first()
    return render(request, 'anime/anime_detail.html', {'anime': anime, 'progress': progress, 'comments': comments, 'comment_form': CommentForm()})

@login_required
def profile(request):
    user = request.user
    progress = UserAnimeProgress.objects.filter(user=user).select_related('anime')
    return render(request, 'profile.html', {'user': user, 'progress': progress})

def accounts_profile_redirect(request):
    return HttpResponseRedirect('/profile/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

@login_required
def add_comment(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.anime = anime
            comment.user = request.user
            comment.save()
            return redirect('anime_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'anime/add_comment.html', {'form': form, 'anime': anime})

@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    slug = comment.anime.slug
    comment.delete()
    return redirect('anime_detail', slug=slug)

class AnimeForm(ModelForm):
    class Meta:
        model = Anime
        fields = ['title', 'description', 'image', 'year', 'genres', 'slug', 'episodes_count']

@staff_member_required
def add_anime(request):
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('anime_list')
    else:
        form = AnimeForm()
    return render(request, 'anime/anime_form.html', {'form': form, 'action': 'Add'})

@staff_member_required
def edit_anime(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            form.save()
            return redirect('anime_detail', slug=slug)
    else:
        form = AnimeForm(instance=anime)
    return render(request, 'anime/anime_form.html', {'form': form, 'action': 'Edit', 'anime': anime})

@staff_member_required
def delete_anime(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    anime.delete()
    return redirect('anime_list')
