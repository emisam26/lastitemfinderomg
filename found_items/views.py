from django.shortcuts import render
from .models import Item
from django.core.paginator import Paginator

# Create your views here.
def items(request):
    items = Item.objects.all()
    paginator = Paginator(items, 4)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)
    context = {
        'items': paged_items
    }
    return render(request, 'found_items/items.html', context)
    # return render(request, 'found_items/items.html')


def item(request, itemid):
    item = Item.objects.get(id=itemid)
    context = {
        'item' : item
    }
    return render(request, 'found_items/item.html', context)