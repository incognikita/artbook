from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadFile, Content
from .forms import CreatePostForm, UploadFileForm, SearchForm


def create_post(request):
    """
    Создание поста.
    Отображение созданных постов в 'homepage'
    """
    user = request.user
    if request.method == 'POST':
        form = CreatePostForm(data=request.POST,
                              files=request.FILES)  # Форма создания поста
        form_file_upload = UploadFileForm(data=request.POST,
                                          files=request.FILES)  # Добавление изображений
        files = request.FILES.getlist('file')  # Все изображения, переданные в форму

        if form.is_valid() and form_file_upload.is_valid():
            content_instance = form.save(commit=False)
            content_instance.author = user  # Указывается автор поста
            content_instance.save()

            for tag in form.cleaned_data['tags']:
                content_instance.tags.add(tag.lower())  # Добавляются теги к посту

            for f in files:
                file_instance = UploadFile(file=f,
                                           content=content_instance)
                file_instance.save()  # Изображения сохряняются в БД
            return redirect('content:create_post')
    else:
        form = CreatePostForm()
        form_file_upload = UploadFileForm()
    return render(request, 'content/create_post.html', {'form': form,
                                                        'form_file_upload': form_file_upload})


def show_post(request, slug, author, pk):
    """Детали поста"""
    post = get_object_or_404(Content,
                             status=Content.Status.PUBLISHED,
                             slug=slug,
                             author=author,
                             pk=pk)
    images = UploadFile.objects.filter(content=pk)
    return render(request, 'content/show_post.html', {'post': post,
                                                      'images': images})
