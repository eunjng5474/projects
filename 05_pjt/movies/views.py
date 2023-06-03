from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm
from django.views.decorators.http import require_http_methods, require_POST


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)

def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {'movie':movie}
    return render(request, 'movies/detail.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                movie = form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm()
        
        context = {'form': form}
        return render(request, 'movies/create.html', context)
    else:
        return redirect('movies:index')


@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', pk=movie.pk)
        else:
            form = MovieForm(instance=movie)
        
        context = {
            'form':form,
            'movie':movie
        }
        return render(request, 'movies/update.html', context)
    return redirect('movies:detail', pk=movie.pk)
        

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        movie.delete()
    return redirect('movies:index')