from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from math import ceil
from .models import Image, Tag, Comment
from .handletags import strip_tagfield
from .forms import ImageForm


# Home view. Display user uploaded images by date. TODO: by views
# Display 20 images at a time by descending order.
# PARAM page = current page of images. (newest images at page no 1 etc)
def upploudhome(request, cur_page=1):
    # TODO: test for negative cur_page, implement fix
    p = (cur_page - 1) * 20
    pn = p + 20
    # calculate the number of image pages.
    max_pages = ceil(Image.objects.all().count() / 20)
    # set variable for next and previous pages. Required for url creation in template
    next_page = cur_page + 1
    prev_page = cur_page - 1
    # Get 20 images in descending order
    images = Image.objects.order_by('-date')[p:pn]
    if not images:
        raise Http404()

    return render(request, 'upploudhome.html', { 'images': images, 'cur_page': cur_page, 'next_page': next_page, 'prev_page': prev_page, 'max_pages': max_pages})


def usersignup(request):
    # redirect to user images instead if logged in
    if request.user.is_authenticated:
        return redirect('/upploud/userimages')

    if request.method == 'POST':
        sform = UserCreationForm(request.POST)
        if sform.is_valid():
            user = sform.save()
            login(request, user)
            return redirect('/upploud/')
    else:
        sform = UserCreationForm()

    return render(request, "signup.html", {'sform': sform})


# display user's uploaded images
def userimages(request):
    return render(request, "userimages.html")


# upload view
def upload(request):
    # Redirect to login page if not logged in.
    if not request.user.is_authenticated:
        return redirect('/upploud/login/')

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()

            # adds tags to image.Tag manytomany field
            strip_tagfield(request.POST.get('tagfield'), image)

            return redirect('/upploud/')
    else:
        form = ImageForm()

    return render(request, "upload.html", {'form': form})


# single image view
def view(request, img_pk):

    img = get_object_or_404(Image, pk=img_pk)
    comments = Comment.objects.filter(image__pk=img.pk)

    # POST handling for comment
    if request.method == 'POST':
        # get the comment
        com = request.POST.get('commentfield')
        # add comment
        newcomment = Comment.objects.create(nick=request.user, comment=com, image=img)
        newcomment.save()

    return render(request, "imageview.html", {'img': img, 'comments': comments})