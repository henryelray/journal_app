from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.


def index(request):
    """Home page of web app"""

    return render(request, 'logs/index.html')


@login_required
def topics(request):
    """Displays all existing topics"""

    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')

    context = {'topics':topics}

    return render(request, 'logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Display a specific topic with its associated entries"""

    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')

    context = {'topic':topic,'topic_id':topic_id, 'entries':entries}

    return render(request, 'logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""

    if request.method != 'POST':
        form = TopicForm()

    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('logs:topics')

    context = {'form':form}

    return render(request, 'logs/new_topic.html', context)


@login_required
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


@login_required
def edit_entry(request, entry_id):
    """Edit an entry"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(instance=entry, data=request.POST)
        entry = form.save(commit=False)

        entry.save()
        return redirect('logs:topic', topic.id)

    context = {'entry':entry,'topic':topic,'form':form}

    return render(request, 'logs/edit_entry.html', context)


def delete_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('logs:topics')

    context = {'entry':entry}
    return render(request, 'logs/delete_entry.html', context)




