from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # For pagination

def set_pagination(request, items):
    """
    Set pagination for a list of items based on the page parameter in the request.

    Args:
    request: The HTTP request object containing the page parameter.
    items: The list of items to be paginated.

    Returns:
    A paginated list of items based on the page parameter in the request. If the page parameter is not provided or is not a valid integer, the first page is returned. If the page parameter exceeds the available pages, the last page is returned.

    Note:
    This function assumes the use of the Django Paginator class with a fixed number of items (99) per page.
    """
    page = request.GET.get('page')

    paginator = Paginator(items, 100)  ## How much news will be shown in each page

    try:
        items = paginator.page(page)

    except EmptyPage:
        items = paginator.page(paginator.num_page)

    except PageNotAnInteger:
        items = paginator.page(1) 
    
    return items