from django.shortcuts import render, redirect
from django.contrib.postgres.search import TrigramSimilarity
from content.models import Content
from content.forms import SearchForm


def homepage(request):
    """Домашняя страница сайта"""

    form = SearchForm()
    query = None
    results = []

    # Поиск контента на главной странице сайте
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Content.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
        return render(request, 'homepage/search_post.html', {'form': form,
                                                             'query': query,
                                                             'results': results})
    else:
        # Отображение постов со статусом 'PUBLISHED на главной странице сайта'
        preview_image = Content.objects.filter(status=Content.Status.PUBLISHED)
        return render(request, 'homepage/homepage.html', {'preview_image': preview_image,
                                                          'form': form})
