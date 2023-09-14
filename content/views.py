from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadFile, Content, Comment
from .forms import CreatePostForm, UploadFileForm, CommentForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage


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
            return redirect('homepage')
    else:
        form = CreatePostForm()
        form_file_upload = UploadFileForm()
    return render(request,
                  'content/create_post.html',
                  {'form': form,
                   'form_file_upload': form_file_upload})


def show_post(request, slug, author, pk):
    """Детали поста"""
    post = get_object_or_404(Content,
                             status=Content.Status.PUBLISHED,
                             slug=slug,
                             author=author,
                             pk=pk)
    images = UploadFile.objects.filter(content=pk)

    # Список активных комментариев к посту
    comments = Comment.objects.filter(content=pk, active=True)
    comment_form = CommentForm()

    # Пагинация
    post_list = Content.published.all()
    paginator = Paginator(post_list, 1)

    page = paginator.page(list(post_list).index(post) + 1)  # Индекс текущего поста в списке всех постов

    try:
        previous_page = post_list[page.previous_page_number() - 1]  # Предыдущая страница относительно текущего поста
    except EmptyPage:
        previous_page = post_list.first()

    try:
        next_page = post_list[page.next_page_number() - 1]  # Следующая страница относительно текущего поста
    except EmptyPage:
        next_page = post_list.last()

    return render(request,
                  'content/show_post.html',
                  {'post': post,
                   'images': images,
                   'form': comment_form,
                   'comments': comments,
                   'previous_page': previous_page,
                   'next_page': next_page, 'page': page})


@require_POST
def post_comment(request, post_id):
    """Создание комментариев"""
    post = get_object_or_404(Content,
                             id=post_id,
                             status=Content.Status.PUBLISHED)
    update_page = Content.published.get(
        title=post.title).get_absolute_url()  # Не уверен что это правильный способ получения url
    # но других вариантов не нашел и не придумал

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content = post
        comment.user = request.user
        comment.save()

    #  После сохранения комментария в бд,
    #  что бы сразу отобразить егоб
    #  происходит редирект на тот же пост

    return redirect(update_page)
