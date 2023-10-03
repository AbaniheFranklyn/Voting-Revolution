from django.contrib import admin
from .models import Candidate,CandidateLevel,PoliticalParty,votingperiod, state, lg,voter,Voting
admin.site.register(Candidate)
admin.site.register(CandidateLevel)
admin.site.register(PoliticalParty)
admin.site.register(votingperiod)
admin.site.register(state)
admin.site.register(lg)
admin.site.register(voter)
admin.site.register(Voting)

# Register your models here.
