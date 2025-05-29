from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Election, Candidate, Voter, Vote, Category
from .forms import VoteForm
from django.db import transaction
# Create your views here.
def voter_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            voter = Voter.objects.get(user=user)
            return redirect('voting', election_id=voter.election.id)
        else:
            messages.error(request, 'Invalid credentials or you have already voted.')
            
    return render(request, 'voting/login.html')


@login_required
def vote(request, election_id):
    try:
        
        
        election = Election.objects.get(id=election_id)
        voter = Voter.objects.get(user=request.user, election=election)
        
        if request.user.is_superuser:
            messages.error(request, 'Only administrators can view results.')
            return redirect('vote-results', election_id=election.id)
        
        if voter.has_voted:
            messages.error(request, 'You have already voted in this election.')
            return redirect('vote-logout')
        

        if request.method == 'POST':
            form = VoteForm(election, request.POST)
            if form.is_valid():
                with transaction.atomic():
                    # Process each category
                    for category in election.categories.all():
                        field_name = f'category_{category.id}'
                        candidate = form.cleaned_data[field_name]
                        Vote.objects.create(
                            election=election,
                            category=category,
                            candidate=candidate,
                            voter=voter
                        )
                
                    # Mark voter as having voted
                    voter.has_voted = True
                    voter.save()
                messages.success(request, 'Your vote has been recorded successfully!')
                return redirect('vote-logout')
        else:
            form = VoteForm(election)
            
        return render(request, 'voting/voting.html', {
            'election': election,
            'form': form
        })
    except (Election.DoesNotExist, Voter.DoesNotExist):
        messages.error(request, 'Invalid election or voter.')
        return redirect('vote-logout')
    
def results(request, election_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can view results.')
        return redirect('vote-login')
    
    election = Election.objects.get(id=election_id)
    categories = Category.objects.filter(election=election).order_by('order')
    
    results_data = []
    for category in categories:
        votes = Vote.objects.filter(election=election, category=category)
        candidates = Candidate.objects.filter(category=category)
        
        candidate_votes = []
        for candidate in candidates:
            vote_count = votes.filter(candidate=candidate).count()
            candidate_votes.append({
                'candidate': candidate,
                'votes': vote_count,
                'percentage': (vote_count / votes.count() * 100) if votes.count() > 0 else 0
            })
            
        results_data.append({
            'category': category,
            'candidates': sorted(candidate_votes, key=lambda x: x['votes'], reverse=True),
            'total_votes': votes.count()
        })
        
    return render(request, 'voting/results.html', {
        'election': election,
        'results': results_data
    })


def voter_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('vote-login')