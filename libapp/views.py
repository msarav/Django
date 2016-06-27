

# Create your views here.
# Import necessary classes

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render
from django.http import HttpResponse
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from libapp.forms import SuggestionForm,SearchlibForm, LoginForm
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test



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
                                                               'item_author':item.author,'item_category':item.category,'user':request.user})
    else:
        return render(request, 'libapp_templates/detail.html',
                      {'item_id': item_id, 'item_type': item_type, 'item_duedate': item.duedate,
                       'item_title': item.title,'item_maker':item.maker,'item_rating':item.rating,'user':request.user})

def abouturls(request):
    # response = HttpResponse()
    # response.write('This is a Library APP.')
    # return response
    return render(request, 'libapp_templates/about.html',{'user':request.user})

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
    return render(request, 'libapp_templates/index.html', {'itemlist': itemlist,'user':request.user})


def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp_templates/suggestions.html', {'itemlist':suggestionlist,'user':request.user})


def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestion'))
        else:
            return render(request, 'libapp_templates/newitem.html', {'form':form, 'suggestions':suggestions,'user':request.user})
    else:
        form = SuggestionForm()
    return render(request, 'libapp_templates/newitem.html', {'form':form, 'suggestions':suggestions,'user':request.user})

def searchlib(request):
    if request.method == 'POST':
        form = SearchlibForm(request.POST)
        message="Please specify appropriate search strings..."

        if form.is_bound:
            if form.is_valid():
                form_data = form.cleaned_data
                author = form_data['author']
                title = form_data['title']
                if len(author) > 0 and len(title)>0:
                    itemlist = Book.objects.filter(title__contains = title,author__contains = author)
                elif len(author) > 0:
                    itemlist = Book.objects.filter(author__contains = author)
                elif len(title)>0:
                    itemlist = Libitem.objects.filter(title__contains = title)
                else:
                    return render(request, 'libapp_templates/searchlib.html', {'form': form, 'message': message,'user':request.user})

                return render(request, 'libapp_templates/searchlib.html', {'form': form, 'itemlist':itemlist,'':"",'user':request.user})

            else:
                return render(request, 'libapp_templates/searchlib.html', {'form': form, 'message': message,'user':request.user})

        else:
            return render(request, 'libapp_templates/searchlib.html', {'form':form, 'message':message,'user':request.user})
    else:
        form = SearchlibForm()
    return render(request, 'libapp_templates/searchlib.html', {'form':form,'user':request.user})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('libapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:

        return render(request, 'libapp_templates/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))

def myitems(request):
    username1 = Libuser.objects.get(username=request.user)
    itemlist = username1.libitem_set.all()
    return render(request, 'libapp_templates/myitems.html',{'itemlist':itemlist,'user':request.user})
