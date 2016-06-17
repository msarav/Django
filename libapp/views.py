from django.shortcuts import render

# Create your views here.
# Import necessary classes
from django.http import HttpResponse
from libapp.models import Book, Dvd, Libuser, Libitem
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def detail(request, item_id):
    # response = HttpResponse()
    # type='Book'
    # try:
    #     item = Book.objects.get(pk=item_id)
    #     p3 = '<p>Author: ' + str(item.author) + '</p>'
    # except Book.DoesNotExist:  # catch the DoesNotExist error
    #     # item = Dvd.objects.get(pk=item_id)
    #     item = get_object_or_404(Dvd, pk=item_id)
    #     type = 'Dvd'
    #     p3 = '<p>Maker: ' + str(item.maker) + '</p>'
    #
    # p = '<p>This is a ' + type + '</p>'
    # p1 = '<p>Title: ' + item.title + '</p>'
    # p2 = '<p>Due Date: ' + str(item.duedate) + '</p>'
    # response.write(p)
    # response.write(p1)
    # response.write(p2)
    # response.write(p3)
    # return response

    type = 'Book'
    try:
        item = Book.objects.get(pk=item_id)
    except Book.DoesNotExist:  # catch the DoesNotExist error
        item = get_object_or_404(Dvd, pk=item_id)
        type = 'Dvd'
    item_type=type

    if type == 'Book':
        return render(request, 'libapp_templates/detail.html',{'item_id':item_id,'item_type':item_type,
                                                                'item_duedate':item.duedate,'item_title':item.title,
                                                               'item_author':item.author,'item_category':item.category})
    else:
        return render(request, 'libapp_templates/detail.html',
                      {'item_id': item_id, 'item_type': item_type, 'item_duedate': item.duedate,
                       'item_title': item.title,'item_maker':item.maker,'item_rating':item.rating})

def abouturls(request):
    # response = HttpResponse()
    # response.write('This is a Library APP.')
    # return response
    return render(request, 'libapp_templates/about.html')

# Create your views here.
# def index(request):
#     response = HttpResponse()
#     booklist = Book.objects.all() [:10]
#     h1 = '<p><b>' + 'Books List: ' + '</b></p>'
#     response.write(h1)
#     for book in booklist:
#         p = '<p><a href="http://127.0.0.1:8000/libapp/detail/' + str(book.id) + '/">'+ str(book) + '</a></p>'
#         response.write(p)
#
#     dvdlist = Dvd.objects.all()[:5]
#     h1 = '<p><b>' + 'DVD List(Normal): ' + '</b></p>'
#     response.write(h1)
#     for dvd in dvdlist:
#         p = '<p><a href="http://127.0.0.1:8000/libapp/detail/' + str(dvd.id) + '">' + str(dvd) + '</a></p>'
#         response.write(p)
#
#     dvdlist = Dvd.objects.all().order_by('-pubyr')[:5]
#     h1 = '<p><b>' + 'DVD List(Ordered): ' + '</b></p>'
#     response.write(h1)
#     for dvd in dvdlist:
#         p = '<p><a href="http://127.0.0.1:8000/libapp/detail/' + str(dvd.id) + '">' + str(dvd) + '</a></p>'
#         response.write(p)
#     return response


def index(request):
    itemlist = Libitem.objects.all().order_by('title')[:10]
    return render(request, 'libapp_templates/index.html', {'itemlist': itemlist})


