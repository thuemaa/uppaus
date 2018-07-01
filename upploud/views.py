from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from math import ceil
from .models import Image, Tag, Comment
from .handletags import strip_tagfield
from .forms import ImageForm


# Home view. Display all uploaded images by date. TODO: by views
# Display 20 images at a time by descending order.
# PARAM page = current page of images. (newest images at page no 1 etc)
# usermode and tagmode: if bool, display the users uploaded images or all images with spesific tag
def thumbnails(request, tag_pk=0, cur_page=1, usermode=False, tagmode=False):
    # TODO: test for negative cur_page, implement fix
    # p: start index, pn: end index
    p = (cur_page - 1) * 20
    pn = p + 20
    # set variable for next and previous pages. Required for url creation in template
    next_page = cur_page + 1
    prev_page = cur_page - 1
    # Get 20 images in descending order by date. Calculate the maximum pages of images
    if usermode and request.user.is_authenticated:
        # change max_pages count to user images maxpage count
        max_pages = ceil(Image.objects.filter(uploaded_by=request.user).count() / 20)
        images = Image.objects.filter(uploaded_by=request.user).order_by('-date')[p:pn]
    elif tagmode and tag_pk != 0:
        tag = Tag.objects.get(pk=tag_pk)
        max_pages = ceil(tag.image_set.all().count() / 20)
        images = tag.image_set.all().order_by('-date')[p:pn]
    else:
        images = Image.objects.order_by('-date')[p:pn]
        max_pages = ceil(Image.objects.all().count() / 20)
    if not images:
        raise Http404()

    return render(request, 'thumbnails.html', {'images': images, 'cur_page': cur_page, 'next_page': next_page, 'prev_page': prev_page, 'max_pages': max_pages, 'usermode': usermode})


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
        return redirect('view', img_pk=img.pk)

    return render(request, "imageview.html", {'img': img, 'comments': comments})

def taglist(request):
    # TODO: exception for 0 tags
    tags = Tag.objects.order_by('name')

    return render(request, "tags.html", {'tags': tags})
