from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer, Comment
from .forms import QuestionCreateForm, AnswerCreateForm, CommentCreateForm
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
@csrf_exempt
def all_questions(request, page_num = 1):
    questions = Question.objects.all().order_by('-created_on')
    p = Paginator(questions, 10)
    current_page = p.page(page_num)
    return render(request, 'qac/index.html', { 'q_list': current_page.object_list, 'page':current_page })


@csrf_exempt
def show_question(request, id = None):
    question_obj = get_object_or_404(Question, id = id)
    user_answer = None
    a_list = None
    if request.user.is_authenticated():
        user_answers = question_obj.answers.filter(created_by=request.user)
        if user_answers:
            user_answer = user_answers[0]
        a_list = question_obj.answers.exclude(created_by=request.user).order_by('-created_on')
    else:
        a_list = question_obj.answers.all().order_by('-created_on')
    context = { 'q': question_obj, 'a_list': a_list, 'a_user': user_answer, 'net_votes': question_obj.upvoted_by.count() - question_obj.downvoted_by.count() }
    return render(request, 'qac/detail.html', context)
    

@require_http_methods(['GET', 'POST'])
@login_required
def add_question(request):
    if request.method == 'GET':
        f = QuestionCreateForm()
    else:
        f = QuestionCreateForm(request.POST)
        if f.is_valid():
            question_obj = f.save(commit = False)
            question_obj.created_by = request.user
            question_obj.save()
            return redirect(reverse('show-question',kwargs={'id': question_obj.id}))
    return render(request, 'qac/add_question.html', {'f': f})

@require_http_methods(['GET', 'POST'])
@login_required
def edit_question(request, id = None):
    question_obj = get_object_or_404(Question, id = id)
    if question_obj.created_by != request.user:
        return redirect(reverse('show-question',kwargs={'id': id }))
    if request.method == 'GET':
        f = QuestionCreateForm(instance = question_obj)
    else:
        f = QuestionCreateForm(request.POST, instance = question_obj)
        if f.is_valid():
            question_obj = f.save()
            return redirect(reverse('show-question',kwargs={'id': id}))
    return render(request, 'qac/edit_question.html', { 'f' : f, 'q_id': id })


@require_http_methods(['GET', 'POST'])
@login_required
def add_answer(request, id = None):
    question_obj = get_object_or_404(Question, id = id)
    if question_obj.created_by == request.user or (request.user.is_authenticated() and question_obj.answers.filter(created_by=request.user)):
        return redirect(reverse('show-question',kwargs={'id': id }))
    if request.method == 'GET':
        f = AnswerCreateForm()
    else:
        f = AnswerCreateForm(request.POST)
        if f.is_valid():
            answer_obj = f.save(commit = False)
            answer_obj.created_by = request.user
            answer_obj.question = question_obj
            answer_obj.save()
            return redirect(reverse('show-question',kwargs={'id': id }))     
    return render(request, 'qac/add_answer.html', {'f': f, 'q_id': id})


@require_http_methods(['GET', 'POST'])
@login_required
def edit_answer(request, id = None, a_id = None):
    question_obj = get_object_or_404(Question, id = id)
    answer_obj = get_object_or_404(Answer, id = a_id)
    if answer_obj.created_by != request.user:
        return redirect(reverse('show-question',kwargs={'id': id }))
    if request.method == 'GET':
        f = AnswerCreateForm(instance = answer_obj)
    else:
        f = AnswerCreateForm(request.POST, instance = answer_obj)
        if f.is_valid():
            answer_obj = f.save()
            return redirect(reverse('show-question',kwargs={'id': id }))
    return render(request, 'qac/edit_answer.html', {'f': f, 'q_id': id, 'a_id': a_id})


@require_http_methods(['GET', 'POST'])
@login_required
def add_question_comment(request, id = None):
    question_obj = get_object_or_404(Question, id = id)
    if request.method == 'GET':
        f = CommentCreateForm()
    else:
        f = CommentCreateForm(request.POST)
        if f.is_valid():
            comment_obj = f.save(commit = False)
            comment_obj.created_by = request.user
            comment_obj.question = question_obj
            comment_obj.save()
            return redirect(reverse('show-question', kwargs={'id': id }))
        
    return render(request, 'qac/add_question_comment.html', {'f': f, 'q_id': id})


@require_http_methods(['GET', 'POST'])
@login_required
def edit_question_comment(request, id = None, c_id = None):
    question_obj = get_object_or_404(Question, id = id)
    comment_obj = get_object_or_404(Comment, id = c_id)
    if comment_obj.created_by != request.user:
        return redirect(reverse('show-question',kwargs={'id': id }))
    if request.method == 'GET':
        f = CommentCreateForm(instance = comment_obj)
    else:
        f = CommentCreateForm(request.POST, instance = comment_obj)
        if f.is_valid():
            comment_obj = f.save()
            return redirect(reverse('show-question',kwargs={'id': id }))
    return render(request, 'qac/edit_question_comment.html', {'f': f, 'q_id': id, 'c_id': c_id })


@require_http_methods(['GET', 'POST'])
@login_required
def add_answer_comment(request, id = None, a_id = None):
    question_obj = get_object_or_404(Question, id = id)
    answer_obj = get_object_or_404(Answer, id = a_id)
    if request.method == 'GET':
        f = CommentCreateForm()
    else:
        f = CommentCreateForm(request.POST)
        if f.is_valid():
            comment_obj = f.save(commit = False)
            comment_obj.created_by = request.user
            comment_obj.answer = answer_obj
            comment_obj.save()
            return redirect(reverse('show-question', kwargs={'id': id }))
        
    return render(request, 'qac/add_answer_comment.html', {'f': f, 'q_id': id, 'a_id': a_id})


@require_http_methods(['GET', 'POST'])
@login_required
def edit_answer_comment(request, id = None, a_id = None, c_id = None):
    question_obj = get_object_or_404(Question, id = id)
    answer_obj = get_object_or_404(Answer, id = a_id)
    comment_obj = get_object_or_404(Comment, id = c_id)
    if comment_obj.created_by != request.user:
        return redirect(reverse('show-question',kwargs={'id': id }))
    if request.method == 'GET':
        f = CommentCreateForm(instance = comment_obj)
    else:
        f = CommentCreateForm(request.POST, instance = comment_obj)
        if f.is_valid():
            comment_obj = f.save()
            return redirect(reverse('show-question',kwargs={'id': id }))
    return render(request, 'qac/edit_answer_comment.html', {'f': f, 'q_id': id, 'a_id': a_id, 'c_id': c_id })


@require_GET
def search_questions(request):
    query_term = request.GET.get('q')
    data = {'questions': []}
    if not query_term:
        return JsonResponse(data)
    questions = Question.objects.filter(
        Q(title__icontains = query_term)|Q(text__icontains = query_term)
    ).order_by('-created_on')
    data['questions'] = [{'id' : q.id, 'title' : q.title , 'created_by' : q.created_by.username } for q in questions]
    return JsonResponse(data)

@require_GET
@login_required
def load_vote_question(request, id=None):
    if request.user.questions_upvoted.filter(id=id):
        return JsonResponse({'result':'up'})
    elif request.user.questions_downvoted.filter(id=id):
        return JsonResponse({'result':'down'})
    return JsonResponse({'result':'none'})


@require_GET
@login_required
def vote_question(request, id=None):
    question_obj = get_object_or_404(Question, id = id)
    di = request.GET.get('dir','')
    if di == 'up':
        switch = request.GET.get('switch','')
        if switch == 'y':
            question_obj.upvoted_by.add(request.user)
            return JsonResponse({'result': 1})
        elif switch == 'n':
            question_obj.upvoted_by.remove(request.user)
            return JsonResponse({'result': -1})
    elif di == 'down':
        switch = request.GET.get('switch','')
        if switch == 'y':
            question_obj.downvoted_by.add(request.user)
            return JsonResponse({'result': -1})
        elif switch == 'n':
            question_obj.downvoted_by.remove(request.user)
            return JsonResponse({'result': 1})
    return JsonResponse({'result': 0})
            
            

