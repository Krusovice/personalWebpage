from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemUploadForm

@login_required(login_url='/login_user/')
def literature_index(request):
    query = request.GET.get('query', '')  # Get search query or default to empty
    items = Item.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(description__icontains=query)
    ) if query else Item.objects.all()

    context = {
        'objects': items,
        'query': query,
        'user': request.user,
    }
    return render(request, 'literature/index.html', context)

@login_required(login_url='/login_user/')
def literature_detail(request, item_id):
    obj = get_object_or_404(Item, id=item_id)
    context = {
        'item': obj,
        'user': request.user,
    }
    return render(request, 'literature/detail.html', context)


@login_required(login_url='/login_user/')
def literature_delete(request, item_id):
    obj = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        obj.delete()
        return redirect(reverse('literature:literature-index'))

    # Render a confirmation page
    context = {'item': obj}
    return render(request, 'literature/confirm_delete.html', context)


@login_required(login_url='/login_user/')
def literature_upload(request):
    if request.method == 'POST':
        form_upload = ItemUploadForm(request.POST, request.FILES)
        if form_upload.is_valid():
            form_upload.save()
            return redirect(reverse('literature:literature-index'))
    else:
        form_upload = ItemUploadForm()

    context = {
        'user': request.user,
        'form_upload': form_upload,
    }
    return render(request, 'literature/upload.html', context)
