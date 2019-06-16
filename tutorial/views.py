# Application(Client) Id : 9f09489f-3698-407b-a821-99320b9fbf5d
# Directory(Tenant) Id : 850aa78d-94e1-4bc6-9cf3-8c11b530701c
# Object Id : f98e7a43-928a-42e2-988d-0c68c4edfb36

# cient secret value for description1 : fm?wXgkxFR2Qij[j5kECGcxFm_HWg?02

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me, make_api_call
import time

# Create your views here.

def home(request):
    redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']
    
    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences

    expiration = int(time.time()) + expires_in - 300
    
    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    return HttpResponse('User: {0}, Access token: {1}'.format(user['displayName'], access_token))



from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def mailing(request):
    html_content = render_to_string('dumb.html', {})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives('reset password', text_content, 'from_mail', ['to_mail'])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    """
    send_mail(
        'This is an auto generated mail',
        'Here is the message.',
        'amritsaha607@gmail.com',
        ['mohnishkumar467@gmail.com'],
        fail_silently=False,
    )
    """
    return HttpResponse("done!")