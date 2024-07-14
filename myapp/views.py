from django.shortcuts import render


# Create your views here.


def base(request):
    return render(request, 'base.html')


def comments(request):
    return render(request, 'comment.html')
