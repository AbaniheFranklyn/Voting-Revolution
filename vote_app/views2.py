from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import CustomUserCreationForm, votingperiod, votingperiodform, CSVUploadForm, VoterForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import PoliticalParty,Candidate,CandidateLevel, state, lg, voter,Voting
from datetime import datetime
from.models import votingperiod
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import csv
import pandas as pd
from django.contrib.auth.models import User 
import smtplib, ssl, getpass
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyperclip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
app_name = 'vote_app'
def generate_token(base_string, token_length):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=token_length-len(base_string)))
    token = base_string + random_string
    token_list = list(token)
    random.shuffle(token_list)
    token = ''.join(token_list)
    return token

def send_token_email(receiver_email, token, fname, cand):
    sender_email = "kingsleyrhema135@gmail.com"
    password = 'mgfzucqoeahfrsea'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Authentication Token"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi,\n\nYour token is: {token}\n\nBest regards,\nKingsley"

    html = f"""\
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.4;
            color: #333;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }}
        h1 {{
            font-size: 24px;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        p {{
            margin: 0 0 10px;
        }}
        b {{
            color: #007bff;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>Hi, {fname}</h1>
        <p>Your token is: <b>{token}</b></p>
        <p>Use this token to vote for the {cand} candidate of your choice.</p>
        <p>Best regards,<br>Kingsley</p>
        </div>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def pres_tvn(request):
    #email= request.user.email
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'PRESIDENTIAL'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
        token = generate_token(base_string, token_length)
        print('President_Token:' + token)
        send_token_email(email, token, fname, cand)
        messages.success(request, 'Token sent to your '+email)
        request.session['token'] = token
        return redirect(reverse('vote_app:pres_tvn'))
    
    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
        user_token = request.POST.get('token-code')
        token = request.session.get('token')
        print('user_token: '+ user_token)
        print(token)
        #print('generated_token: '+ generate_token())
        if user_token == token:
            messages.success(request, 'Token Verified')
            return HttpResponseRedirect(reverse('vote_app:pres'))
        else:
            messages.error(request, 'Try again token does not match')
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_pres.html',context)

def gov_tvn(request):
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'GOVERNOR'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
            token = generate_token(base_string, token_length)
            print('Governor_Token:' + token)
            send_token_email(email, token, fname, cand)
            messages.success(request, 'Token sent to your '+email)
            request.session['token'] = token
            return HttpResponseRedirect(reverse('vote_app:gov_tvn'))

    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
            user_token = request.POST.get('token-code')
            token = request.session.get('token')
            #print(token)
            #print('generated_token: '+ generate_token())
            if user_token == token:
                messages.success(request, 'Token Verified')
                return HttpResponseRedirect(reverse('vote_app:gov'))
            else:
                messages.error(request, 'Try again token does not match')    
    
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_gov.html',context)
    
    
    
def chm_tvn(request):
        #email= request.user.email
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'LOCAL GOVERNMENT CHAIRMAN'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
            token = generate_token(base_string, token_length)
            print('Local Gov_Token:' + token)
            send_token_email(email, token, fname, cand)
            messages.success(request, 'Token sent to your mail @' +email)
            request.session['token'] = token
            return redirect(reverse('vote_app:chm_tvn'))
    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
            user_token = request.POST.get('token-code')
            token = request.session.get('token')
            #print(token)
            #print('generated_token: '+ generate_token())
            if user_token == token:
                messages.success(request, 'Token Verified')
                return HttpResponseRedirect(reverse('vote_app:lgc'))
            else:
                messages.error(request, 'Try again token does not match')    
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_chm.html',context)

def hoa_tvn(request):
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'HOUSE OF ASSEMBLY'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
            token = generate_token(base_string, token_length)
            print('House Of Ass_Token:' + token)
            send_token_email(email, token, fname, cand)
            messages.success(request, 'Token sent to your '+email)
            request.session['token'] = token
            return redirect(reverse('vote_app:hoa_tvn'))
    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
            user_token = request.POST.get('token-code')
            token = request.session.get('token')
            #print(token)
            #print('generated_token: '+ generate_token())
            if user_token == token:
                messages.success(request, 'Token Verified')
                return HttpResponseRedirect(reverse('vote_app:hoa'))
            else:
                messages.error(request, 'Try again token does not match')    
    
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_hoa.html',context)

def hor_tvn(request):
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'HOUSE OF REPRESENTATIVE'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
            token = generate_token(base_string, token_length)
            print('House Of Rep_Token:' + token)
            send_token_email(email, token, fname, cand)
            messages.success(request, 'Token sent to your '+email)
            request.session['token'] = token
            return redirect(reverse('vote_app:hor_tvn'))
    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
            user_token = request.POST.get('token-code')
            token = request.session.get('token')
            #print(token)
            #print('generated_token: '+ generate_token())
            if user_token == token:
                messages.success(request, 'Token Verified')
                return HttpResponseRedirect(reverse('vote_app:hor'))
            else:
                messages.error(request, 'Try again token does not match')    
    
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_hor.html',context)

def senate_tvn(request):
    email = request.user.email
    fname = request.user.voter.firstname
    lname = request.user.voter.secondname
    vin = request.user.voter.vin
    cand = 'SENATORAL'
    base_string = fname + lname + str(vin)
    token_length = 16
    if request.method == 'POST' and request.POST.get('get-token') == 'submit':
            token = generate_token(base_string, token_length)
            print('Senate_Token:' + token)
            send_token_email(email, token, fname, cand)
            messages.success(request, 'Token sent to your '+email)
            request.session['token'] = token
            return redirect(reverse('vote_app:senate_tvn'))
    elif request.method == 'POST' and request.POST.get('verify-token') == 'submit':
            user_token = request.POST.get('token-code')
            token = request.session.get('token')
            #print(token)
            #print('generated_token: '+ generate_token())
            if user_token == token:
                messages.success(request, 'Token Verified')
                return HttpResponseRedirect(reverse('vote_app:senate'))
            else:
                messages.error(request, 'Try again token does not match')    
    
    context = {'email':email,'fname':fname,'lname':lname,'vin':vin}
    return render(request,'vote_app/token_senate.html',context)

