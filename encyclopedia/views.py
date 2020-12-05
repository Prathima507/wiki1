import random
import re
from django import forms
from django.shortcuts import render
from .import util
from markdown2 import Markdown
from django.urls import reverse

markdowner = Markdown()


class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(attrs={"rows":10,"cols":20}), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={"rows":10,"cols":20}), label='')


"""
index function will return with all the available pages in encyclopedia
"""
def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }
                return render(request, "encyclopedia/entry.html", context)
               
            if item.lower() in i.lower():
                searched.append(i)
                context = {
                        'searched': searched,
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })

"""
If the user types with different names in search page then if it is available then its shown or else page not found is displayed.
"""
def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)

        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"form":Search(), "message": "The requested page was not found."})

"""
If user want to go for new page in encyclopedia then create function is used.
New Pages are created.
"""

def create(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "Page already exist"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)

                context = {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                }

                return render(request, "encyclopedia/entry.html", context)

    else:
        return render(request, "encyclopedia/create.html", {"form": Search(), "post": Post()})

"""
If user want to edit changes to the available page then can edit the page,
 if any changes are done then its converted to markdown page and is stored in encyclopedia.
 """


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)

        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)

            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }

            return render(request, "encyclopedia/entry.html", context)
            

"""
If user wants to display any random page then random Page function is used.
"""
def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdowner.convert(page)

        context = {
            'form': Search(),
            'page': page_converted,
            'title': page_random
        }

        return render(request, "encyclopedia/entry.html", context)
