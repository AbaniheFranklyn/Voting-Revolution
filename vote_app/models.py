from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib import request


class CandidateLevel(models.Model):
    level_name = models.CharField(max_length=100)
    def __str__(self):
        return self.level_name 

class state(models.Model):
    state = models.CharField(max_length=200)
    def __str__(self):
        return self.state


class lg(models.Model):
    lgs = models.CharField(max_length=200)
    state = models.ForeignKey(state, on_delete=models.CASCADE) 
    def __str__(self):
        return self.lgs

class PoliticalParty(models.Model):
    party_name = models.CharField(max_length=100)
    party_logo = models.ImageField(upload_to='vote_app/static/images/logos')
    candidate_level = models.ForeignKey(CandidateLevel, on_delete=models.CASCADE)
    
    # def __str__(self):
    #         name = self.party_name
    #         cand = self.candidate_level
    #         return name,cand
    def __str__(self):
        return f"{self.party_name} {self.candidate_level}"



class Candidate(models.Model):
    name = models.CharField(max_length=100)
    manifesto = models.TextField()
    political_party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} Party: {self.political_party.party_name} Candidate Level: {self.political_party.candidate_level}"

class votingperiod(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class voter(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=150)
    secondname = models.CharField(max_length=150)
    vin = models.CharField(max_length=11)
    state = models.CharField(max_length=50)
    local_government = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.firstname} {self.secondname} - {self.state} - {self.local_government}"
    
    
class Voting(models.Model):
    voter = models.ForeignKey(voter, on_delete=models.CASCADE)
    party = models.CharField(max_length=255)
    candidate_level = models.CharField(max_length=255)
    candidate_name = models.CharField(max_length=255, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    v_state = models.CharField(max_length=100, default=False)
    v_lg = models.CharField(max_length=100, default=False)
    voted = models.BooleanField(default=False)
    vote_hash = models.CharField(max_length=225,default=False)
    previous_vote_hash = models.CharField(max_length=225, default = False)
    def __str__(self):
        return f"{self.voter.firstname} {self.voter.secondname} - votes {self.party} for {self.candidate_level}"
    





# @receiver(post_save, sender=voter)
# def mapVoter(sender, instance, created, **kwargs):
#     if created:
#         user_profile = instance.user
#         instance.user = user_profile.user
#         instance.save()
#         print(instance)
      
