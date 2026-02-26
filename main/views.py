from django.shortcuts import render

# Create your views here.
def home(request):
    links = [
        {"name": "Сторінка 1", "url": "/page1/"},
        {"name": "Сторінка 2", "url": "/page2/"},
    ]

    context = {
        "title": "Головна сторінка",
        "content": "Це головна сторінка",
        "links": links
    }

    return render(request, "main/index.html", context)


def page1(request):
    context = {
        "title": "Сторінка 1",
        "content": "Це перша сторінка.",
        "links": [{"name": "На головну сторінку", "url": "/"}]
    }

    return render(request, "main/index.html", context)


def page2(request):
    context = {
        "title": "Сторінка 2",
        "content": "Це друга сторінка.",
        "links": [{"name": "На головну стрінку", "url": "/"}]
    }

    return render(request, "main/index.html", context)