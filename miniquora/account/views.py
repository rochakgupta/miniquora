from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from .forms import LoginForm, ForgotPassword, SetPasswordForm, SignupForm, ProfileForm
from .models import MyUser, create_otp, get_valid_otp_object
from django.core.paginator import Paginator
from django.db.models import Q
from qac.models import Question


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('all-questions'))
    next_page = request.GET.get('next',reverse('all-questions'))
    if request.method == 'GET':
        context = { 'f' : LoginForm(), 'next_page' : next_page}
        return render(request, 'account/auth/login.html', context)
    else:
        f = LoginForm(request.POST)
        if not f.is_valid():
            context = { 'f' : f, 'next_page' : next_page}
            return render(request, 'account/auth/login.html', context)
        else:
            user = f.authenticated_user
            auth_login(request, user)
            return redirect(next_page)
        
def forgot_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('all-questions'))
    if request.method == 'GET':
        context = { 'f' : ForgotPassword()}
        return render(request, 'account/auth/forgot_password.html', context)
    else:
        f = ForgotPassword(request.POST)
        if not f.is_valid():
            return render(request, 'account/auth/forgot_password.html', {'f' : f})
        else:
            user = MyUser.objects.get(username = f.cleaned_data['username'])
            otp = create_otp(user = user, purpose = 'FP')
            email_body_context = { 'u' : user, 'otp' : otp}
            body = loader.render_to_string('account/auth/email/forgot_password.txt', email_body_context)
            message = EmailMultiAlternatives("Reset Password", body, settings.EMAIL_HOST_USER, [user.email])
            #message.attach_alternative(html_body, 'text/html')
            message.send()
            return render(request, 'account/auth/forgot_email_sent.html', {'u': user})

def reset_password(request, id = None, otp = None):
    if request.user.is_authenticated():
        return redirect(reverse('all-questions'))
    user = get_object_or_404(MyUser, id=id)
    otp_object = get_valid_otp_object(user = user, purpose='FP', otp = otp)
    if not otp_object:
        raise Http404()
    if request.method == 'GET':
        f = SetPasswordForm()
    else:
        f = SetPasswordForm(request.POST)
        if f.is_valid():
            user.set_password(f.cleaned_data['new_password'])
            user.save()
            otp_object.delete()
            return render(request, 'account/auth/set_password_success.html', { 'u' : user})
    context = { 'f' : f, 'otp': otp_object.otp, 'uid': user.id}
    return render(request, 'account/auth/set_password.html', context)

@require_GET
@login_required
def home(request, id=None , page_num = 1):
    questions = Question.objects.filter(created_by = request.user).order_by('-created_on')
    p = Paginator(questions, 2)
    current_page = p.page(page_num)
    return render(request, 'account/auth/home.html', { 'q_list': current_page.object_list, 'page':current_page })


@require_GET
@login_required
def search_my_questions(request, id=None):
    query_term = request.GET.get('q')
    data = {'questions': []}
    if not query_term:
        return JsonResponse(data)
    questions = request.user.questions_created.filter(
        Q(title__icontains = query_term)|Q(text__icontains = query_term)
    ).order_by('-created_on')
    data['questions'] = [{'id' : q.id, 'title' : q.title, 'text' : q.text } for q in questions]
    return JsonResponse(data)


def logout(request):
    next_page = request.GET.get('next',reverse('all-questions'))
    auth_logout(request)
    return redirect(next_page)

def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse('all-questions'))
    if request.method == 'GET':
        context = { 'f' : SignupForm()}
        return render(request, 'account/auth/signup.html', context)
    else:
        f = SignupForm(request.POST)
        if not f.is_valid():
            return render(request, 'account/auth/signup.html', {'f' : f})
        else:
            user = f.save(commit = False)
            user.set_password(f.cleaned_data['password'])
            user.is_active = False
            user.save()
            otp = create_otp(user = user, purpose = 'AA')
            email_body_context = { 'u' : user, 'otp' : otp}
            body = loader.render_to_string('account/auth/email/activate_account.txt', email_body_context)
            message = EmailMultiAlternatives("Activate Account", body, settings.EMAIL_HOST_USER, [user.email])
            message.send()
            return render(request, 'account/auth/activation_email_sent.html', {'u': user})

@require_GET
def activate(request, id = None, otp = None):
    if request.user.is_authenticated():
        return redirect(reverse('all-questions'))
    user = get_object_or_404(MyUser, id=id)
    otp_object = get_valid_otp_object(user = user, purpose='AA', otp = otp)
    if not otp_object:
        raise Http404()
    user.is_active = True
    user.save()
    otp_object.delete()
    return render(request, 'account/auth/activation_success.html', { 'u' : user})


@require_http_methods(['GET', 'POST'])
@login_required
def edit_profile(request, id=None ):
    if request.method == 'GET':
        f = ProfileForm(instance = request.user)
    else:
        f = ProfileForm(request.POST, instance = request.user)
        if f.is_valid():
            user = f.save(commit = False)
            if f.cleaned_data['new_password']:
                user.set_password(f.cleaned_data['new_password'])
            user.save()
            return redirect(reverse('home',kwargs={'id': id}))
    return render(request, 'account/user/profile.html', {'f': f, 'u_id': id})

