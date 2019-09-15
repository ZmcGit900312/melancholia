from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    like_dict = {"boldmessage":"大香蕉，大苹果，大桃子，大猩猩"}
    return render(request,'rango/index.html',context=like_dict)
    #return HttpResponse("Hello, Fuck Body!<br/> <a href='/rango/about/'>About</a>")

def about(request):
    return render(request,'rango/about.html')
