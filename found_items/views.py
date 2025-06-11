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

def save_model(self, request, obj, form, change):
    super().save_model(request, obj, form, change)  # Save normally
    
    # Build paths
    file_path = obj.photo.path  # local file path after save
    supabase_path = f"photos/{os.path.basename(file_path)}"
    
    # Upload to supabase
    public_url = upload_to_supabase(file_path, supabase_path)
    if public_url:
        obj.supabase_url = public_url
        obj.save(update_fields=['supabase_url'])
