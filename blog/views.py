from django.shortcuts import render
from .models import SimpleBook,ContentImage
# Create your views here.

def display_book(request):
    book = SimpleBook.objects.last()
    
    
    return render(request,'index.html',{'book':book})
