from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from contests.models import Contest, ContestQuestion
from questions.models import Question
from .forms import HostContestForm, ContestQuestionForm
from questions.forms import PostQuestionForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from registration.views import email_confirmation_required

# Create your views here.
@login_required
@email_confirmation_required
def contest_question_create(request, contest_unique_id=None):
    contest_id = get_object_or_404(Contest, unique_code=contest_unique_id)
    if (contest_id.author != request.user):
        return PermissionDenied("You can not post question in this contest!")
    if (request.method == "POST"):
        form = PostQuestionForm(request.POST)
        contest_question_points= ContestQuestionForm(request.POST)
        if form.is_valid() and contest_question_points.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.active = False
            question.save()
            contest_question = contest_question_points.save(commit=False)
            contest_question.contest = contest_id
            contest_question.question = question
            contest_question.save()
            return HttpResponse("Successfully added question in contest!!!")
    else:
        form = PostQuestionForm()
        contest_question_points= ContestQuestionForm()
    context = {
        'form': form,
        'cq': contest_question_points,
    }
    return render(request, 'contests/create_contest_question.html', context)


@login_required
@email_confirmation_required
def contest_question_edit(request, contest_unique_id, question_unique_id):
    question_instance=get_object_or_404(Question, unique_code=question_unique_id)
    contest_instance=get_object_or_404(Contest, unique_code=contest_unique_id)
    instance = get_object_or_404(ContestQuestion, question=question_instance, contest=contest_instance)
    form = PostQuestionForm(request.POST or None, instance=question_instance, initial={"category":question_instance.category})
    contest_question_points= ContestQuestionForm(request.POST or None, instance=instance)
    if form.is_valid() and contest_question_points.is_valid():
        points= contest_question_points.cleaned_data["points"]
        contest_question_form = form.save(commit=False)
        contest_question_form.save()
        contest_question_points.save()
        return HttpResponse("Successfully edited question in contest!!!")
    context = {
    'form': form,
    'cq': contest_question_points
    }
    return render(request, "contests/create_contest_question.html", context)

@login_required
@email_confirmation_required
def create_contest(request):
    if (request.method == "POST"):
        form = HostContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.author = request.user
            contest.save()
            return HttpResponse('contest saved!!')
        else:
            print(form.errors)
    else:
        form = HostContestForm()
    return render(request, 'contests/create_contest.html', {'form':form})

@login_required
@email_confirmation_required
def edit_contest(request, contest_unique_id):
    instance = get_object_or_404(Contest, unique_code=contest_unique_id)
    if instance.author != request.user:
        return PermissionDenied("You can not edit this question!")
    form = HostContestForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponse("edited!!")
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, "contests/create_contest.html", context)
def view_contest_page(request, contest_unique_code):
	contest = get_object_or_404(Contest, unique_code= contest_unique_code)
	return render(request, 'contest_page.html', {'contest': contest})
