from django.shortcuts import render
from .models import Topic, Entry
# Create your views here.


def index(request):
    """Home page of web app"""

    return render(request, 'logs/index.html')


def topics(request):
    """Displays all existing topics"""

    topics = Topic.objects.order_by('-date_added')

    context = {'topics':topics}

    return render(request, 'logs/topics.html', context)


def topic(request, topic_id):
    """Display a specific topic"""

    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.order_by('-date_added')

    context = {'topic':topic,'topic_id':topic_id, 'entries':entries}

    return render(request, 'logs/topic.html', context)