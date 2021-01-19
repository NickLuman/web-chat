from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views import View

from .models import Chat, Message
from .forms import LoginForm, UserRegistrationForm, MessageForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/chat/me')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})

@login_required
def user_logout(request): 
    logout(request)
    return render(request, 'chat/logged_out.html')

def auth_check(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/chat/me')
        else:
            return redirect('/chat/login')

@login_required
def dashboard(request):
    if request.method == 'GET':

        username = request.GET.get('q')
        if username is not None:
            if username == request.user.username:
                return HttpResponse('You have entered your username!')
            try:
                user = User.objects.get(username=username)
                return render(request, 'chat/found_user.html', {'user_id': user.id, 'username': username})
            except User.DoesNotExist:
                return HttpResponse('User isn\'t found')

    return render(request, 'chat/dashboard.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/chat/login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'chat/register.html', {'user_form': user_form})

class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except:
            chat = None
        
        form = MessageForm()
        return render(
            request,
            'chat/user_chat.html',
            {
                'chat': chat,
                'form': form,
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(request.POST)
        if form.is_valid():
            user_message = Message()
            user_message.message = form.cleaned_data['message']
            user_message.chat = Chat.objects.get(id=chat_id)
            user_message.author = request.user
            user_message.save()
        return redirect('/chat/me/dialogue/{0}'.format(chat_id), {'chat_id', chat_id})


class CreateDialogueView(View):
    def get(self, request, user_id):
        chk_sum = request.user.id + user_id
        
        chats = Chat.objects.filter(check_sum=chk_sum)

        if chats.count() == 0:
            chat = Chat(check_sum=chk_sum)
            chat.save()
            chat.members.add(request.user)
            user = User.objects.get(id=user_id)
            chat.members.add(user)
            chat.save()
        else:
            chat = chats.first()
        return redirect('/chat/me/dialogue/{0}'.format(chat.id))