from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

@login_required
def image_create(request):
    """
    View to handle image creation.
    """
    if request.method == 'POST':
        # form is submitted
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the image
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully.')
            # redirect to the image detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

def image_detail(request, id, slug):
    """
    View to display image details.
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})

@require_POST
@login_required
def image_like(request):
    """
    View to handle liking an image.
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok', 'total_likes': image.users_like.count()})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
def image_list(request):
    """
    View to list all images with pagination.
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)  # Show 8 images per page
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    # try to get the requested page
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # if AJAX request and page is out of range, return empty list
            return HttpResponse('')
        # if page is out of range, deliver last page of results
        images = paginator.page(paginator.num_pages)
    if images_only:
        # if AJAX request, return only the images
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
