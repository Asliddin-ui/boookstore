from datetime import datetime, timedelta
from datetime import datetime
from django.db import connection
from django.shortcuts import HttpResponse, Http404
from .models import *
from django.db.models import Q, F, Avg, Count, Max, Min, Case, OuterRef, Subquery, Value, When, Sum
from django.db.models.functions import Length, Left
from django.utils.translation import gettext_lazy as _

def index(request):
    return HttpResponse(_('Ok'))


def categories(request, id):

    if id == 1:
        result = []
        for b in Books.objects.order_by('-added_at').all():
            result.append(f"{b.id}:{b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 2:
        result = []
        for b in Books.objects.filter(added_at__year=datetime.now().year, read = 0):
            result.append(f"{b.id}:{b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 3:
        result = []
        for b in Books.objects.filter(added_at__year=datetime.now().year-1).order_by('-read')[:10]:
            result.append(f"{b.id}:{b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 4:
        return HttpResponse(Books.objects.filter(status=1).count())

    elif id == 5:
        result = []
        for b in Books.objects.filter(language__in=(1, 2), publish_year=2005).order_by('?')[:10]:
            result.append(f"{b.id}:{b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 6:
        result = []
        for b in Books.objects.order_by('price', '-read')[:10]:
            result.append(f"{b.id}:{b.name} | {b.price}")
        return HttpResponse("<br/>".join(result))

    elif id == 7:
        result = []
        #print(Books.objects.annotate(rating = F("rating_stars")/F('rating_count')).filter(added_at__month=1).order_by('-rating').query)
        for b in Books.objects.annotate(rating = F("rating_stars")/F('rating_count')).filter(added_at__month=1).order_by('-rating'):
            result.append(f"{b.id}:{b.name} | {b.added_at} | {b.rating}")
        return HttpResponse("<br/>".join(result))

    elif id == 8:
        result = []
        for b in Books.objects.filter(added_at=F('update_at')).order_by('added_at')[:10]:
            result.append(f"{b.id}:{b.name} | {b.price}")
        return HttpResponse("<br/>".join(result))
    elif id == 9:
        result = []
        for b in Books.objects.annotate(rating = F('rating_stars')/F('rating_count'),name_len=Length('name')).filter(name_len__lte=5).order_by('rating')[:10]:
            result.append(f"{b.id}:{b.name} | {b.rating}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 10:
        result = []
        for b in Books.objects.filter(publish_year__in=[2010,2015,2020]):
            result.append(f"{b.id}:{b.name} | {b.publish_year}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 11:
        result = []
        for b in Books.objects.filter(publish_year__gte=datetime.now().year-3).order_by('-price'):
            result.append(f"{b.id}:{b.name} | {b.publish_year}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 12:
        result = []
        for b in Books.objects.annotate(rating = F('rating_stars')/F('rating_count')).order_by('-price', 'rating'):
            result.append(f"{b.id}:{b.name} | {b.publish_year} | {b.rating}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 13:
        result = []
        for b in Books.objects.filter(read__gte=F('reading')).order_by('id'):
            result.append(f"{b.id}:{b.name} | {b.publish_year} | {b.read} | {b.will_read}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 14:
        result = []
        for b in Books.objects.exclude(added_at = F('update_at')).order_by('-update_at')[:10]:
            result.append(f"{b.id}:{b.name} | {b.publish_year}")
        return HttpResponse("<br/>".join(result))

    elif id == 15:
        result = []
        for b in Books.objects.filter(name__istartswith="A").order_by('?')[:10]:
            result.append(f"{b.id}:{b.name} | {b.name}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 16:
        result = []
        for b in Books.objects.filter(name__istartswith="De", category_id__in=[1,2,3]).order_by('?')[:10]:
            result.append(f"{b.id}:{b.name} | {b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 17:
        result = []
        for b in Books.objects.annotate(raiting=F('rating_stars')/F('rating_count')).filter(language_id__in = [1,2]).order_by('-raiting')[:10]:
            result.append(f"{b.id}:{b.name} | {b.name} | {b.raiting}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 18:
        result = []
        for b in Books.objects.annotate(raiting=F('rating_stars')/F('rating_count')).filter(country_id = 1, language_id__gt =1).order_by('-raiting')[:10]:
            result.append(f"{b.id}:{b.name} | {b.name} | {b.raiting}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 19:
        result = []
        for b in Books.objects.filter(Q(name__istartswith='A') | Q(name__istartswith='R') |
                                       Q(name__istartswith='S'), availability=0).exclude(country_id=1):
            result.append(f"{b.id}:{b.name} | {b.name}")
        return HttpResponse("<br/>".join(result))

    elif id == 20:
        result = []
        for b in Books.objects.filter(read=F('reading'), reading=F('will_read'), read__gt=0):
            result.append(f"{b.id}:{b.name} | {b.name}")
        return HttpResponse("<br/>".join(result))
    





    elif id == 21:
        result = []
        print(Books.objects.values('category_id').annotate(min_price = Min('price')).query)
        for b in Books.objects.values('category_id').annotate(min_price = Min('price'))[:10]:
            result.append(f"{b['category_id']} | {b['min_price']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 22:
        result = []
        print(Books.objects.values('category_id', 'language_id').annotate(count = Count('id')).query)
        for b in Books.objects.values('category_id', 'language_id').annotate(count = Count('id')).order_by('category_id'):
            result.append(f"{b['category_id']} | {b['language_id']} | {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 23:
        result = []
        #print(Books.objects.values('category_id', 'language_id').annotate(count = Count('id')).query)
        for b in Books.objects.values('publish_year').annotate(max_read = Max('read')).filter(publish_year__gt=datetime.now().year-10):
            result.append(f"{b['publish_year']} | {b['max_read']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 24:
        result=[]
        for b in Books.objects.values(name_alfa = Left('name',1)).annotate(max_rating = Max(F('rating_stars')/F('rating_count'))):
            result.append(f"{b['name_alfa']} | {b['max_rating']}")
        return HttpResponse("<br/>".join(result))

    elif id == 25:
        result=[]
        for b in Books.objects.values(name_alfa = Left('name',1)).annotate(count = Count('id')):
            result.append(f"{b['name_alfa']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 26:
        result=[]
        for b in Books.objects.values('status').annotate(count = Count('id')):
            result.append(f"{b['status']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 27:
        result=[]
        for b in Books.objects.values('added_at__year').annotate(count = Count('id')):
            result.append(f"{b['added_at__year']} | {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 28:
        result=[]
        for b in Books.objects.annotate(rating = F('rating_stars')/F('rating_count'), rating_btw = Case(
            When(Q(rating__gt=4) & Q(rating__lte=5), then=Value('4-5')),
            When(Q(rating__gt=3) & Q(rating__lte=4), then=Value('3-4')),
            When(Q(rating__gt=2) & Q(rating__lte=3), then=Value('2-3')),
            When(Q(rating__gt=1) & Q(rating__lte=2), then=Value('1-2')),
            default=Value('0-1')
        )).values('rating_btw').annotate(books_count = Count('id')):
            result.append(f"{b['rating_btw']} | {b['books_count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 29:
        result = []
        for b in Books.objects.values('added_at__month').annotate(count = Count('id')):
            result.append(f"{b['added_at__month']} | {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 30:
        result = []
        for b in Books.objects.values('status','availability').annotate(count = Count('id')):
            result.append(f"{b['status']} | {b['availability']} | {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 31:
        result=[]
        for b in Books.objects.annotate(price_status = Case(
            When(Q(price__gte=1000000), then=Value('Qimmat')),
            When(Q(price__gt=100000) & Q(price__lte=1000000), then=Value('O`rtacha')),
            default=Value('Arzon')
        )).values('price_status').annotate(count = Count('id')):
            result.append(f"{b['price_status']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 32:
        result=[]
        for b in Books.objects.annotate(price_status = Case(
            When(Q(price__gte=1000000), then=Value('Qimmat')),
            When(Q(price__gt=100000) & Q(price__lte=1000000), then=Value('O`rtacha')),
            default=Value('Arzon')
        )).values('country__name', 'price_status').annotate(count = Count('id')):
            result.append(f"{b['country__name']} | {b['price_status']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 33:
        result=[]
        for b in Books.objects.annotate(price_status = Case(
            When(Q(price__gte=1000000), then=Value('Qimmat')),
            When(Q(price__gt=100000) & Q(price__lte=1000000), then=Value('O`rtacha')),
            default=Value('Arzon')
        )).values('country__name', 'language__lang', 'price_status').annotate(count = Count('id')):
            result.append(f"{b['country__name']} | {b['language__lang']} | {b['price_status']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 34:
        result=[]
        b = Books.objects.annotate(price_status = Case(
            When(Q(price__gte=1000000), then=Value('Qimmat')),
            When(Q(price__gt=100000) & Q(price__lte=1000000), then=Value('O`rtacha')),
            default=Value('Arzon')
        )).values('id', 'name', 'price', 'price_status').order_by('price')
        a = b.filter(price_status = 'Arzon').union(b.filter(price_status='Qimmat'), b.filter(price_status='O`rtacha'))
        # print(b.filter(price_status = 'Arzon').union(b.filter(price_status='Qimmat'), b.filter(price_status='O`rtacha')).query)
        for a in b:
            result.append(f"{a['id']} | {a['name']} | {a['price']} | {a['price_status']}")
        return HttpResponse("<br/>".join(result))


        # books = Books.objects.annotate(price_status = Case(
        #         When(Q(price__gte = 1000000), then=Value("Qimmat")),
        #         When(Q(price__lte = 100000), then=Value("Arzon")),
        #         default=Value("O`rtacha")
        #     )).values("id", "name", "price", "price_status").order_by("price")
        # books.filter(price_status = "Arzon").union(books.filter(price_status = "O`rtacha"), books.filter(price_status = "Qimmat"))
        # print(books.filter(price_status = "Arzon").union(books.filter(price_status = "O`rtacha"), books.filter(price_status = "Qimmat")).query)
        # for b in books:
        #     result.append(f"{b['id']} | {b['name']} | {b['price']} | {b['price_status']}")

        # return HttpResponse("<br/>".join(result))
    
    elif id == 35:
        result=[]
        for b in Books.objects.annotate(rating = F('rating_stars')/F('rating_count'), price_status = Case(
            When(Q(price__gte=1000000), then=Value('Qimmat')),
            When(Q(price__gt=100000) & Q(price__lte=1000000), then=Value('O`rtacha')),
            default=Value('Arzon')
        ), 
            rating_btw = Case(
            When(Q(rating__gt=4) & Q(rating__lte=5), then=Value('4-5')),
            When(Q(rating__gt=3) & Q(rating__lte=4), then=Value('3-4')),
            When(Q(rating__gt=2) & Q(rating__lte=3), then=Value('2-3')),
            When(Q(rating__gt=1) & Q(rating__lte=2), then=Value('1-2')),
            default=Value('0-1')
            )
        ).values('price_status', 'rating_btw').annotate(count = Count('id')).order_by('count'):
            result.append(f"{b['price_status']} ({b['rating_btw']}) : {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 36:
        result = []
        for b in Books.objects.values('name').annotate(books_count = Count('id')).exclude(books_count=1):
            result.append(f"{b['name']} | {b['books_count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 37:
        result = []
        for b in Books.objects.values('publish_year', 'language__lang').annotate(count = Count('id')).order_by('publish_year'):
            result.append(f"{b['publish_year']} | {b['language__lang']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 38:
        result = []
        for b in Books.objects.values('category__name').annotate(count = Count('id')).filter(rating_count = 0).order_by("category"):
            result.append(f"{b['category__name']} | {b['count']}")
        return HttpResponse("<br/>".join(result))

    elif id == 39:
        result = []
        for b in Books.objects.values('category__name', 'language__lang').annotate(count = Count('id')).filter(rating_count = 0).order_by("category"):
            result.append(f"{b['category__name']} | {b['language__lang']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 40:
        result = []
        for b in Books.objects.values('publish_year').annotate(count = Count('id')).order_by("-count")[:3]:
            result.append(f"{b['publish_year']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 41:
        return HttpResponse(str(Books.objects.aggregate(ortacha_narx = Avg("price"))))
    
    elif id == 42:
        result = []
        for b in Books.objects.values('category__name').annotate(count = Count('id')).filter(category__name__istartswith = 'D').order_by("count"):
            result.append(f"{b['category__name']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 43:
        result = []
        for b in Books.objects.values('language__lang').annotate(count = Count('id')).order_by("count"):
            result.append(f"{b['language__lang']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 44:
        result = []
        for b in Books.objects.values('authors__name').annotate(count = Count('id')).filter(authors__name__istartswith = 'a').order_by("count"):
            result.append(f"{b['authors__name']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 45:
        rating = F('rating_stars')/F('rating_count')
        return HttpResponse(str(Books.objects.aggregate(ortacha_rating = Avg(rating))))
    
    elif id == 46:
        result = []
        rating = F('rating_stars')/F('rating_count')
        for b in Books.objects.values('category__name').annotate(count = Avg(rating),min = Min(rating),max = Max(rating)):
            result.append(f"{b['category__name']} | {b['count']} | {b['min']} | {b['max']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 47:
        result = []
        for b in Books.objects.values('language__lang').annotate(reading = Sum('reading'), will_read = Sum('will_read'), read = Sum('read')):
            result.append(f"{b['language__lang']} | {b['read']} | {b['reading']} | {b['will_read']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 48:
        result = []
        for b in Books.objects.values('authors__name').annotate(young = Min('publish_year'), max = Max('publish_year')):
            result.append(f"{b['authors__name']} | {b['young']} | {b['max']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 49:
        result = []
        for b in Books.objects.values('category__name').annotate(count = Count('authors')).filter(count = 2):
            result.append(f"{b['category__name']} | {b['count']}")
        return HttpResponse("<br/>".join(result))
    
    elif id == 50:
        result = []
        category = Category.objects.filter(id = OuterRef("category_id"), name__startswith = 'F')
        # for b in Books.objects.annotate(cid = Subquery(category.values('id'))).filter(category_id = F('cid')).aggregate(Avg('price'))
        return HttpResponse(str(Books.objects.annotate(cid = Subquery(category.values('id'))).filter(category_id = F('cid')).aggregate(Avg('price'))))
    else:
        return HttpResponse('Page mavjud emas')


pass