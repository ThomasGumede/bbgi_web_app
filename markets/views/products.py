from django.shortcuts import render, get_object_or_404, redirect

def shop(request):
    return render(request, "coming-soon.html")