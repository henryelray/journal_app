from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
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
    """Display a specific topic with its associated entries"""

    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.order_by('-date_added')

    context = {'topic':topic,'topic_id':topic_id, 'entries':entries}

    return render(request, 'logs/topic.html', context)


def new_topic(request):
    """Add a new topic"""

    if request.method != 'POST':
        form = TopicForm()

    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('logs:topics')

    context = {'form':form}

    return render(request, 'logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry"""

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()

    else:

        form = EntryForm(data=request.POST)
        if form.is_valid():

            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logs:topic', topic_id=topic_id)

    context = {'form':form, 'topic':topic}

    return render(request, 'logs/new_entry.html', context)


def edit_entry(request, entry_id):
    """Edit an entry"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(instance=entry, data=request.POST)
        entry = form.save(commit=False)
        entry.save()
        return redirect('logs:topic', topic.id)
    context = {'entry':entry,'topic':topic,'form':form}

    return render(request, 'logs/edit_entry.html', context)



