from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown
from pathlib import Path
from . import util
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':20, 'cols':100}),label=False)

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':20, 'cols':100}),label=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random_page(request):
    #gen random name
    random_name = random.choice(util.list_entries())
    return redirect('/wiki/'+random_name)

def load_entry(request, entry_name):
    md = markdown.Markdown(extensions=["fenced_code"])
    # check if entry_name exists
    if entry_name in util.list_entries():
        #get markdown content
        markdown_content = Path("entries/"+entry_name+".md").read_text()
        markdown_content = md.convert(markdown_content)
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_name,
            "markdown_content": markdown_content
    })
    else:
        return render(request, "encyclopedia/error.html", {
            "markdown_content": md.convert(Path("entries/invalid/InvalidEntry.md").read_text())
    })

def create_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] in util.list_entries():
                print("PAGE EXISTS")
                return HttpResponseRedirect(reverse('error_create'))
            else:
                #write content to markdown file
                Path("entries/"+form.cleaned_data["title"]+".md").write_text(form.cleaned_data["content"])
                return HttpResponseRedirect(reverse('entry', kwargs={'entry_name': form.cleaned_data["title"]}))
    else:
        #render HTML with form
        return render(request, "encyclopedia/create.html", {
                "form": NewEntryForm({'title': 'Enter title here', 'content': 'Enter content here'})
         })

def error_creating_page(request):
    md = markdown.Markdown(extensions=["fenced_code"])
    return render(request, "encyclopedia/error.html", {
            "markdown_content": md.convert(Path("entries/invalid/InvalidCreate.md").read_text())
    })

def edit_page(request, entry_name):

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
        #write content to markdown file
            Path("entries/"+entry_name+".md").write_text(form.cleaned_data["content"])
            return HttpResponseRedirect(reverse('entry', kwargs={'entry_name': entry_name}))
    else:
        return render(request, "encyclopedia/edit.html", {
                "entry_title": entry_name,
                "form": EditEntryForm({'content': Path("entries/"+entry_name+".md").read_text()})
        })

def search(request):

    if request.method == "POST":
        search_word = request.POST['q']
        all_entries = util.list_entries()
        search_entries = []
        #get entries matching search
        for entry in all_entries:
            if search_word == entry:
                return HttpResponseRedirect(reverse('entry', kwargs={'entry_name': search_word}))
            if search_word in entry:
                search_entries.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "entries": search_entries
        })
