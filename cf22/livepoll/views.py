from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.urls import reverse
from .models import Poll, Answer
from django.utils import timezone
from .forms import PollForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json

# The following four functions render their
# respective pages with no special content
# or conditions that affect the page.
def home(request):
    page = 'livepoll/home.html'
    return render(request, page)

def redirect_to_home(request):
    return redirect('home')

def about(request):
    page = 'livepoll/about.html'
    return render(request, page)

def devlog(request):
    page = 'livepoll/devlog.html'
    return render(request, page)

# This function renders a page with a
# list of polls ordered by the date posted.
def polls(request):
    poll_list = Poll.objects.all()
    page = 'livepoll/polls.html'
    content = {'poll_list':poll_list}
    return render(request, page, content)

# This function handles ajax requests sent by the
# "live" page. This sends data to the page so the
# pie chart can update in real time.
def get_data(request):

    if request.method == 'GET':
        poll_id = request.GET['poll_id']

        poll = get_object_or_404(Poll, pk=poll_id)
        answer_list = poll.answer_set.all()

        answer = 'Answer'
        votes = 'Votes'

        data = [[answer, votes]]
        for answer in answer_list:
            data.append([answer.text, answer.votes])

        data_array = json.dumps(data)

        return HttpResponse(data_array)

# This function renders the "live" page
# with a specific poll and corresponding answers.
def live(request, poll_ID):
    poll = get_object_or_404(Poll, pk=poll_ID)
    answer_list = poll.answer_set.all()
    page = 'livepoll/live.html'
    content = {
        'poll':poll,
        'answer_list':answer_list,
    }

    return render(request, page, content)

# This function renders the page where users
# vote on the poll they selected. If the user
# tries to access this page without being logged
# in, they will be redirected to the login page.
@login_required
def question(request, poll_ID):
    poll = get_object_or_404(Poll, pk=poll_ID)
    answer_list = poll.answer_set.all()
    page = 'livepoll/question.html'

    voter = request.user
    previous_voters = poll.voter.all()

    # If the user has already voted on this poll, redirect
    # them to the live results page for the poll.
    # Superusers (admins) can vote as much as they like.
    if voter in previous_voters and voter.is_superuser == False:
        return HttpResponseRedirect(reverse('live', args=(poll.pk,)))

    content = {
    'poll':poll,
    'answer_list':answer_list,
    }

    # If the poll has less than 2 options to vote on, send
    # a message that the poll is unavaible. (The question.html
    # page won't render if it detects the 'error' key)
    if len(answer_list) < 2:
        content['error'] = "Poll is currently unavailable."

    # If the user didn't vote on the poll and the poll has
    # 2 or more answers, render the voting page.
    return render(request, page, content)

# This function is called when the user presses
# the "Vote" button on the voting page. It
# updates the corresponding model to reflect
# the updated number of votes.
def vote(request, poll_ID):
    poll = get_object_or_404(Poll, pk=poll_ID)
    try:
        choice = poll.answer_set.get(pk=request.POST['option'])
    except:
        # If the user votes without selecting an option,
        # redirect them to the voting page with an error message.
        page = 'livepoll/question.html'
        answer_list = poll.answer_set.all()
        content = {
            'poll':poll,
            'answer_list':answer_list,
            'error':"Choose an option first!"
        }
        return render(request, page, content)
    else:
        # Update votes. Add user to list of voters.
        choice.votes += 1
        choice.save()
        poll.voter.add(request.user)

    # If the user's vote went through, redirect them to the
    # live tally page for the poll they just voted on.
    return HttpResponseRedirect(reverse('live', args=(poll.pk,)))

# This functions renders a form for
# creating a new user account
def register(request):
    # If request = Post, save new account
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account successfully created.')
            return redirect('create_account')
    # If request = Get, render a new account form
    else:
        user_form = UserCreationForm()
    page = 'livepoll/create_account.html'
    return render(request, page, {'form':user_form})

# This function allows a user to create a new poll.
# If the user tries to access this page without
# being logged in, they will be redirected to
# the login page.
@login_required
def new_poll(request):
    # If request = Post, save new post
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.post_date = timezone.now()
            poll.creator = request.user
            poll.save()
            # Once the poll has been created, render the
            # page for adding answer options to their poll
            return redirect('new_answer', poll_ID=poll.pk)
    # If request = Get, render a new poll form
    else:
        poll_form = PollForm()
    page = 'livepoll/new_poll.html'
    return render(request, page, {'form':poll_form})

# This function allows a user to create a new answer
# for the poll they're in the process of creating.
@login_required
def new_answer(request, poll_ID):
    page = 'livepoll/new_answer.html'

    poll = get_object_or_404(Poll, pk=poll_ID)

    creator = (Poll.objects.get(pk=poll_ID)).creator
    if request.user != creator:
        page = 'livepoll/home.html'
        return render(request, page, {'message':' * You can\'t edit other people\'s polls!'})

    if request.method == "POST":

        # grab data from submitted form
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():

            answer = answer_form.save(commit=False)
            answer.poll = poll
            answer.save()

            answer_num = len(poll.answer_set.all())
            messages = []

            # notify user whether they have hit the minimum answers for their poll
            # and whether they successfully added an answer
            if answer_num < 2 and answer_num > 0:
                messages.append(" * You need to have at least two answers")
                messages.append(" * Successfully added answer")
            else:
                messages.append(" * Successfully added answer")
                messages.append(" * Once you're done adding answers, go to the \
                polls page to check out your poll")

            answer_form = AnswerForm()
            content = {
                'messages':messages,
                'form':answer_form,
            }

            # notify the user that they hit the answer limit for their poll
            if (answer_num == 6):
                content['error'] = """
                                    * You have reached the maximum number of
                                   answers for your poll.
                                   """

            # render a blank new form so the user can add another answer
            return render(request, page, content)
    else:
        answer_form = AnswerForm()

    # initial rendering of blank form with message to notify user
    # that they need a minimum of two answers to their poll
    messages = ["* You need to have at least two answers"]
    content = {
        'messages':messages,
        'form':answer_form,
    }
    return render(request, page, content)

# This function renders a page that shows the user a list
# of their polls, as well as an option to edit them by
# adding more answers.
@login_required
def profile(request):
    user = request.user
    page = 'livepoll/profile.html'
    poll_list = Poll.objects.filter(creator=user)
    content = {
        'user':user,
        'poll_list':poll_list
    }
    return render(request, page, content)
