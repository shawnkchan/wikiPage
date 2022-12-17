import re
from django.shortcuts import render, redirect
from django.contrib import messages
from . import util
import encyclopedia
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    page = util.get_entry(title)

    if page == None:
        return render(request, 'encyclopedia/error.html',{
            'title': title
        })
    return render(request, 'encyclopedia/page.html',{
            'title': title,
            'page': markdown2.markdown(page)
        })

def search(request):
    simPages = []
    result = request.POST['q'].upper() #use GET request to retrieve the variable named 'q'
    if result not in [entry.upper() for entry in util.list_entries()]:
        for entry in util.list_entries():
            if result in entry.upper():
                simPages.append(entry)
        return render(request, 'encyclopedia/searchRes.html', {
            'title': entry,
            'pages': simPages
        })
    return page(request, result)

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if title.upper() in [entry.upper() for entry in util.list_entries()]:
            messages.error(request, 'The wiki entry already exists')
        else:
            util.save_entry(title, content)
            return page(request, title)
    return render(request, 'encyclopedia/create.html')

def edit(request, title):
    reqPage = util.get_entry(title)
    
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        return page(request, title)
    else:
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'page': reqPage
        })

def randomPage(request): #cant name this 'random' as it overrides the imported function
    entries = util.list_entries()
    randPage = entries[random.randint(0,len(entries)-1)]
    return page(request, randPage)
