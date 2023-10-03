from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import CustomUserCreationForm, votingperiod, votingperiodform, CSVUploadForm, VoterForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import PoliticalParty,Candidate,CandidateLevel, state, lg, voter, Voting
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




import hashlib
import datetime

class vote_in:
    def __init__(self, index, timmestamp, vote_data, previous_hash):
        self.index = index
        self.timestamp = timmestamp
        self.vote_data = vote_data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8')+
                   str(self.timestamp).encode('utf-8')+
                   str(self.vote_data).encode('utf-8')+
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
class VoteChain:
    def __init__(self):
        self.chain= [self.create_genesis_vote()]
    
    def create_genesis_vote(self):
        return vote_in(0, datetime.datetime.now(), "Genesis Block", "0")
    
    def get_latest_vote(self):
        return self.chain[-1]
            
    
    def add_vote(self,new_vote):
        new_vote.previous_hash = self.get_latest_vote().hash
        new_vote.hash = new_vote.calculate_hash()
        self.chain.append(new_vote)

    def is_vote_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_vote = self.chain[i]
            previous_vote = self.chain[i-1]
            if current_vote.hash != current_vote.calculate_hash():
                return False
            if current_vote.previous_hash != previous_vote.hash:
                return False
        return True

def logout_now(request):
    logout(request)
    return HttpResponseRedirect(reverse('vote_app:home'))

def login(request):
    return render(request, 'vote_app/login.html')

def signup(request):
    if request.method != 'POST':
        form = CustomUserCreationForm()
        form2 = VoterForm()
    else:
        form = CustomUserCreationForm(request.POST)
        form2 = VoterForm(request.POST)
        if form.is_valid() and form2.is_valid():
            new_user = form.save()
            new_voter = form2.save(commit=False)
            new_voter.user = new_user
            new_voter.save()
            #new_voter.save()
            messages.success(request, "Successful registration")
            authenticated_user = authenticate(username= new_user.username, password = request.POST['password1'])
            auth_login(request, authenticated_user)
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    states=state.objects.order_by('state')
    lgs=lg.objects.order_by('lgs')
    context = {'form':form, 'form2':form2,'states':states,'lgs':lgs}
    return render(request, 'vote_app/signup.html',context)


@login_required
def vote(request):
    now = timezone.now()
    try:
        period = votingperiod.objects.get()
        print("start_date:", period.start_date)
        print("end_date:", period.end_date)
        if period.start_date <= now and now <= period.end_date:
            # voting is allowed
            time_remaining = period.end_date - now
            parties = PoliticalParty.objects.order_by('party_name')
            candidates = Candidate.objects.order_by('name')
            candidateslevel = CandidateLevel.objects.order_by('level_name')
            voters = voter.objects.get(user=request.user)
            context = {'parties':parties, 'candidates':candidates, 'remaining_time': str(time_remaining), 'candidateslevel':candidateslevel}
            voting_in_pres = Voting.objects.filter(voter=request.user.voter, candidate_level='PRESIDENT')
            voting_in_gov = Voting.objects.filter(voter=request.user.voter, candidate_level='GOVERNOR')
            voting_in_senate = Voting.objects.filter(voter=request.user.voter, candidate_level='SENATOR')
            voting_in_hoa = Voting.objects.filter(voter=request.user.voter, candidate_level='HOUSE OF ASSEMBLY')
            voting_in_hor = Voting.objects.filter(voter=request.user.voter, candidate_level='HOUSE OF REP')
            voting_in_lgc = Voting.objects.filter(voter=request.user.voter, candidate_level='LOCAL GOV. CHAIRMAN')
            if request.method == 'POST' and request.POST.get('get-token-pres') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='PRESIDENT')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:pres_tvn'))

            elif request.method == 'POST' and request.POST.get('get-token-gov') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='GOVERNOR')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:gov_tvn'))

            elif request.method == 'POST' and request.POST.get('get-token-senate') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='SENATOR')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:senate_tvn'))

            elif request.method == 'POST' and request.POST.get('get-token-hor') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='HOUSE OF REP')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:hor_tvn'))

            elif request.method == 'POST' and request.POST.get('get-token-hoa') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='HOUSE OF ASSEMBLY')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:hoa_tvn'))

            elif request.method == 'POST' and request.POST.get('get-token-chm') == 'submit':
                voting_instance = Voting.objects.filter(voter=request.user.voter, candidate_level='LOCAL GOV. CHAIRMAN')
                if voting_instance:
                    return HttpResponseRedirect(reverse('vote_app:voted'))
                else:
                    return HttpResponseRedirect(reverse('vote_app:chm_tvn'))

            if voting_in_pres and voting_in_gov and voting_in_senate and voting_in_hoa and voting_in_hor and voting_in_lgc: 
                return HttpResponseRedirect(reverse('vote_app:thank')) 
            return render(request, 'vote_app/vote.html', context)
        elif now < period.start_date:
            return render(request, 'vote_app/vote_not_started.html',{'period':period})
        else:
            # voting has ended
            return render(request, 'vote_app/vote_closed.html')
    except votingperiod.DoesNotExist:
        # no voting period set up yet
        return render(request, 'vote_app/vote_not_started.html')




def thank(request):
    return render(request, 'vote_app/thank.html')




def base(request):
    return render(request, 'vote_app/base.html')





def results(request):
    now = timezone.now()
    period = votingperiod.objects.get()
    if period.start_date <= now and now <= period.end_date:
        time_remaining = period.end_date
        return render(request, 'vote_app/vote_started.html',{'period':period,'time_remaining':time_remaining})
    else:
        return render(request, 'vote_app/result.html')
    




@staff_member_required
def setvote(request):
    try:
        period = votingperiod.objects.get()
    except votingperiod.DoesNotExist:
        period = None
    if request.method == 'POST':
        form = votingperiodform(request.POST, instance=period)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vote_app:setvote'))
    else:
        form = votingperiodform(instance=period)
    return render(request,'vote_app/setvote.html', {'form':form})

csv_file_path = '/static/LGs/LGAs in Nigeria.csv'
@staff_member_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            statee = []
            r = 0.5
            csv_file = pd.read_csv(request.FILES['csv_file'])
            for i in csv_file:
                statee.append(i)
            for i in statee:
                for y in csv_file[i]:
                    if type(y) != type(r):
                        state_obj, _ = state.objects.get_or_create(state=i)
                        lg_obj = lg.objects.create(lgs=y, state=state_obj)
            return render(request, 'vote_app/upload_gov.html', {'form': form, 'success': True})
    else:
        form = CSVUploadForm()
    return render(request, 'vote_app/upload_gov.html', {'form': form})

def gov(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg},""))   
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, v_state=voter_state,v_lg=voter_lg, voted = True)
        voters.save()
        return HttpResponseRedirect(reverse('vote_app:vote'))
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/gov.html',context)

def pres(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg,'vote_hash':block.hash,'previous_vote_hash':block.previous_hash},""))
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        if votechain.is_vote_chain_valid:    
            Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, voted = True)
            voters.save()
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request,'The vote has been tampered with')
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
            
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/pres.html',context)

def senate(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg},""))
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        if votechain.is_vote_chain_valid:    
            Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, voted = True)
            voters.save()
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request,'The vote has been tampered with')
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
            
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/senate.html',context)

def chm(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg},""))
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        if votechain.is_vote_chain_valid:    
            Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, voted = True)
            voters.save()
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request,'The vote has been tampered with')
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
            
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/chm.html',context)

def hor(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg},""))
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        if votechain.is_vote_chain_valid:    
            Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, voted = True)
            voters.save()
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request,'The vote has been tampered with')
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/hor.html',context)

def hoa(request):
    parties = PoliticalParty.objects.order_by('party_name')
    candidates = Candidate.objects.order_by('name')
    candidateslevel = CandidateLevel.objects.order_by('level_name')
    voters = voter.objects.get(user=request.user)
    if request.method == 'POST' and request.POST.get('vote') == 'submit':
        party = request.POST.get('candidate_party')
        level = request.POST.get('candidate_level')
        cand_name = request.POST.get('candidate_name')
        voter_vin = voters.vin
        voter_state = request.user.voter.state
        voter_lg = request.user.voter.local_government
        vote_time = datetime.datetime.now()
        votechain = VoteChain()
        votechain.add_vote(vote_in(str(vote_time),datetime.datetime.now(),{'Voter Vin':voter_vin, 'Voted Party':party, 'Candiate Level':level, 'Voter State':voter_state, 'Voter Local Gvernment':voter_lg},""))
        for block in votechain.chain[1:]:
            print("Block: ", block.index)
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.vote_data)
            print("Hash: ", block.hash)
            print("Previous Hash: ", block.previous_hash)
            print("------------")
        if votechain.is_vote_chain_valid:    
            Voting.objects.create(voter=voters, party=party, candidate_level=level, candidate_name = cand_name, voted = True)
            voters.save()
            return HttpResponseRedirect(reverse('vote_app:vote'))
        else:
            messages.error(request,'The vote has been tampered with')
            #return redirect(HttpResponseRedirect('vote_app:vote_tamp'))
            
    context = {'parties':parties, 'candidates':candidates,'voter':voters, 'candidateslevel':candidateslevel}
    return render(request,'vote_app/hoa.html',context)

def voted(request):
    return render(request, 'vote_app/voted.html')


