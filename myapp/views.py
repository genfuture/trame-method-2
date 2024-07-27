from django.shortcuts import render

def trame_view(request):
    return render(request, 'trame.html')
