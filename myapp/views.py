from django.shortcuts import render, redirect
from .forms import CommentForm

# Create your views here.


def base(request):
    return render(request, 'base.html')


# def comments(request):
#     return render(request, 'comment.html')



def comments(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comments')
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form})
