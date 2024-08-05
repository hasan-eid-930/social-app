from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from inbox.form import MessageCreateForm
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from inbox.models import Conversation
from users.models import Profile
from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models import Q
# get current user model  
User=get_user_model()

# my ciphar
f = Fernet(settings.ENCRYPT_KEY)


@login_required
def inbox(request,conversation_id=None):
    my_conversations=request.user.conversations.all()
    if conversation_id:
        conversation=get_object_or_404(my_conversations,pk=conversation_id)
        last_message=conversation.messages.last()
        if conversation.is_seen == False and last_message.sender != request.user:
            conversation.is_seen=True
            conversation.save()
    else:
        conversation=None
    form=MessageCreateForm()
    context={
        'my_conversations':my_conversations,
        'conversation':conversation,
        'form':form,
    }
    if request.htmx:
        return render(request,'inbox/partials/conversation_part.html',context)
    
    return render(request,'inbox/inbox.html',context)

def search_user(request):
    name=request.GET.get('user_search')
    if request.htmx:
        if len(name)>0:
            profiles=Profile.objects.filter(realname__icontains=name)
            # get users id for profiles thier realname contains name 
            user_ids=profiles.values_list('user_id',flat=True)
            users=User.objects.filter(Q(username__icontains=name)|Q(id__in=user_ids) ).exclude(username=request.user.username)
            return render(request,'inbox/partials/searchusers_part.html',{"users":users})
        else:
            # return empty page
            return HttpResponse('')
    else:
        raise Http404("page does not exist")

@login_required
def new_message(request,recipient_name):
    recipient=get_object_or_404(User,username=recipient_name)
    # to prevent users from message themself
    if recipient != request.user:
        if request.method=='POST':
            form=MessageCreateForm(request.POST)
            if form.is_valid():
                # returm model instance without saving it to db
                message = form.save(commit=False)
                # encrypt message
                message_original = form.cleaned_data['body']
                # convert message to binary
                message_bytes = message_original.encode('utf-8')
                # encrypt message
                message_encrypted = f.encrypt(message_bytes)
                # decode encrypted message to string to be able to store it in db
                message_decoded = message_encrypted.decode('utf-8')
                message.body = message_decoded
                
                message.sender=request.user
                # return first conversation contain recipient in its participients
                my_conversations=request.user.conversations.all()
                for conversation in my_conversations:
                    if recipient in conversation.participants.all():
                        message.conversation=conversation
                        break
                # if we use conversation_id because foriegnkey relation
                if not message.conversation_id:
                    conversation=Conversation.objects.create(admin=request.user)
                    conversation.participants.add(request.user,recipient)
                    conversation.save()
                    message.conversation=conversation
                message.save()
                conversation.last_message_at=timezone.now()
                conversation.is_seen=False
                conversation.save()
                return redirect('conversation',message.conversation.id)
        form=MessageCreateForm()
        context={
            'form':form,
            'recipient':recipient,
        }
        if request.htmx:
            return render(request,'inbox/create_message.html',context)
    else:
        raise Http404('')
@login_required
def send_reply(request,conversation_id):
    my_conversations=request.user.conversations.all()
    conversation=get_object_or_404(my_conversations,pk=conversation_id)
    if request.htmx:
        form=MessageCreateForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            # encrypt message
            message_original = form.cleaned_data['body']
            message_bytes = message_original.encode('utf-8')
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode('utf-8')
            message.body = message_decoded

            message.sender=request.user
            message.conversation=conversation
            message.save()
            conversation.last_message_at=timezone.now()
            conversation.is_seen=False
            conversation.save()
            return render(request,'inbox/partials/message_part.html',{'message':message})
        
    return redirect('conversation',conversation.id)


def check_notification(request,conversation_id):
    conversation=get_object_or_404(Conversation,pk=conversation_id)
    last_message=conversation.messages.last()
    if conversation.is_seen == False and last_message.sender != request.user:
        return render(request,'inbox/partials/notification.html')
    else:
        return HttpResponse('')

def inbox_notify(request):
    unseen_conversation=request.user.conversations.filter(is_seen=False)
    for conversation in unseen_conversation:
        last_message=conversation.messages.last()
        if request.user != last_message.sender:
            return render(request,'inbox/partials/notification.html',{'inbox':True})
    return HttpResponse('')