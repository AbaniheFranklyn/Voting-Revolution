from django.shortcuts import render
from django.db.models import Count
from .models import Voting, PoliticalParty

def result_pres(request):
    president_votes = Voting.objects.filter(candidate_level='PRESIDENT').values('party').annotate(total_votes=Count('id'))
    parties = PoliticalParty.objects.all()
    results = {}
    for party in parties:
        results[party.party_name] = 0
    for vote in president_votes:
        results[vote['party']] = vote['total_votes']
    context = {
        'results': results
    }
    return render(request, 'vote_app/result_pres.html', context)


def result_gov(request):
    # get all unique states from Voting objects
    states = Voting.objects.values_list('v_state', flat=True).distinct()
    
    if request.method == 'POST':
        # get the selected state from the POST request
        selected_state = request.POST.get('state')

        # get the governor votes for the selected state
        governor_votes = Voting.objects.filter(candidate_level='GOVERNOR', v_state=selected_state).values('party').annotate(total_votes=Count('id'))
        context = {'states': states, 'governor_votes': governor_votes, 'selected_state': selected_state}
    else:
        context = {'states': states}
    
    return render(request, 'vote_app/result_gov.html', context)

def result_hor(request):
    states = Voting.objects.filter(candidate_level='HOUSE OF REP').values_list('v_state', flat=True).distinct()
    if request.method == 'POST':
        selected_state = request.POST['state']
        house_rep_votes = Voting.objects.filter(candidate_level='HOUSE OF REP', v_state=selected_state).values('party').annotate(total_votes=Count('id'))
    else:
        house_rep_votes = []
        selected_state = None

    context = {
        'states': states,
        'house_rep_votes': house_rep_votes,
        'selected_state': selected_state,
    }
    return render(request, 'vote_app/result_hor.html', context)

def result_hoa(request):
    states = Voting.objects.filter(candidate_level='HOUSE OF ASSEMBLY').values_list('v_state', flat=True).distinct()
    if request.method == 'POST':
        state = request.POST['state']
        hoa_votes = Voting.objects.filter(candidate_level='HOUSE OF ASSEMBLY', v_state=state).values('party').annotate(total_votes=Count('id'))
        return render(request, 'vote_app/result_hoa.html', {'states': states, 'state': state, 'hoa_votes': hoa_votes})
    return render(request, 'vote_app/result_hoa.html', {'states': states})

def result_lgc(request):
    # get distinct list of states from Voting table
    states = Voting.objects.values_list('v_state', flat=True).distinct()
    
    if request.method == 'GET':
        # if form is submitted, get the selected state and its results
        selected_state = request.GET.get('state', None)
        if selected_state:
            lg_votes = Voting.objects.filter(candidate_level='LOCAL GOVERNMENT CHAIRMAN', v_state=selected_state).values('party').annotate(total_votes=Count('id'))
            context = {'states': states, 'selected_state': selected_state, 'lg_votes': lg_votes}
            return render(request, 'vote_app/result_chm.html', context)

    # if form is not submitted, just show the states list
    context = {'states': states}
    return render(request, 'vote_app/result_chm.html', context)

def result_senate(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        senate_votes = Voting.objects.filter(candidate_level='SENATOR', v_state=state).values('party').annotate(total_votes=Count('id'))
        context = {'senate_votes': senate_votes, 'state': state}
        return render(request, 'vote_app/result_senate.html', context)
    else:
        return render(request, 'vote_app/result_senate.html')