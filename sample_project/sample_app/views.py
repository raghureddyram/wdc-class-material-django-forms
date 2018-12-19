from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from .forms import BookForm

from .models import Author, Book


def index(request):
    sort_method = request.GET.get('sort', 'asc')
    books = Book.objects.all()
    if sort_method == 'asc':
        books = books.order_by('popularity')
    elif sort_method == 'desc':
        books = books.order_by('-popularity')

    if 'q' in request.GET:
        q = request.GET['q']
        books = books.filter(title__icontains=q)
    return render(request, 'index.html', {
        'books': books,
        'authors': Author.objects.all(),
        'sort_method': sort_method,
    })


def create_book(request):
    authors = Author.objects.all()
    if request.method == 'GET':
        book_form = BookForm
        return render(request, 'create_book.html', {'book_form': book_form})
    elif request.method == 'POST':
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            Book.objects.create(**book_form.cleaned_data)
            return redirect('/')
       
        return redirect('/')


def edit_book(request, book_id=None):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method=='GET':
         book_form = BookForm(instance=book)
         context = {
             'book': book,
             'book_form': book_form
         }
         return render(request, 'edit_book.html', context)

    if request.method == 'POST':
        book_form = BookForm(request.POST)
       
        if book_form.is_valid():
            book_form.save()
            return redirect('/')


def delete_book(request):
    book_id = request.POST.get('book_id')

    book = get_object_or_404(Book, id=book_id)

    book.delete()
    return redirect('/')


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {
        'authors': authors
    })


def author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound()

    return render(request, 'author.html', {
        'author': author
    })
