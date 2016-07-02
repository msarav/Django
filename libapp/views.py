

# Create your views here.
# Import necessary classes
import random
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse

from django.shortcuts import render,render_to_response
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from libapp.forms import SuggestionForm,SearchlibForm, LoginForm, RegisterForm
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

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

    if 'about_visits' in request.COOKIES:
        visitcount = int(request.COOKIES['about_visits'])+1
    else:
        visitcount=1

    response = render(request, 'libapp_templates/about.html', {'user': request.user, 'visits': visitcount})
    response.set_cookie('about_visits', visitcount, max_age=300)
    return response

def index(request):
    luckynum = 0
    if 'luckynum' in request.session:
        luckynum = request.session['luckynum']  # __getitem__

    itemlist = Libitem.objects.all().order_by('title')[:10]
    return render(request, 'libapp_templates/index.html', {'itemlist': itemlist,'user':request.user,'luckynum':luckynum})


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
        message = ""
    return render(request, 'libapp_templates/searchlib.html', {'form':form,'user':request.user,'message':message})


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                luckynum = random.randint(1, 9)
                request.session['luckynum'] = luckynum
                request.session.set_expiry(60 * 60)
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
    itemlist=[]
    message=''
    try:
        username1 = Libuser.objects.get(username=request.user)
        itemlist = username1.libitem_set.all()
        message = "You've checkout the below items..."
    except:
        message="You are not a Libuser"
    return render(request, 'libapp_templates/myitems.html',{'itemlist':itemlist,'user':request.user,'message':message})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            usr_obj = form.save(commit=False)
            usr_obj.user_image = request.POST['user_image']
            usr_obj.save()

            return HttpResponseRedirect(reverse('libapp:login'))
        else:
            return render(request, 'libapp_templates/newitem.html',
                          {'form': form, 'user': request.user})
    else:
        form=RegisterForm()
        return render(request, 'libapp_templates/register.html',{'form':form})

def sug_detail(request, item_id):
    item = Suggestion.objects.get(pk=item_id)
    return render(request, 'libapp_templates/sug_detail.html',{'item':item})
