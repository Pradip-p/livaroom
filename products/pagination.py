from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # For pagination

def set_pagination(request, items):
    page = request.GET.get('page')

    paginator = Paginator(items, 99)  ## How much news will be shown in each page

    try:
        items = paginator.page(page)

    except EmptyPage:
        items = paginator.page(paginator.num_page)

    except PageNotAnInteger:
        items = paginator.page(1) 
    
    return items