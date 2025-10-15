import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Election, Candidate, Voter, Vote, Category
from .forms import VoteForm, VoterUploadForm
from django.db import transaction
from django.views import View
from django.contrib.auth.models import User
import string
import secrets
from django.contrib.auth.hashers import make_password

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


def upload_voters(request):
    if request.method == 'POST':
        form = VoterUploadForm(request.POST, request.FILES)
        if form.is_valid():
            election = form.cleaned_data['election']
            json_file = request.FILES['json_file']
            use_custom_passwords = form.cleaned_data['use_custom_passwords']
            default_password = form.cleaned_data['default_password']
            
            # Validate default password if not using custom passwords
            if not use_custom_passwords and not default_password:
                messages.error(request, "Default password is required when not using custom passwords")
                return render(request, 'voting/upload_voters.html', {'form': form})
            
            try:
                # Read and parse the JSON file
                file_content = json_file.read().decode('utf-8')
                voter_data = json.loads(file_content)
                
                success_count = 0
                error_count = 0
                errors = []
                
                with transaction.atomic():
                    for index, voter_info in enumerate(voter_data):
                        try:
                            # Extract voter information
                            username = voter_info.get('username')
                            email = voter_info.get('email')
                            unique_key = voter_info.get('unique_key')
                            custom_password = voter_info.get('password')
                            
                            # Validate required fields
                            if not all([username, email, unique_key]):
                                error_count += 1
                                errors.append(f"Row {index + 1}: Missing required fields (username, email, or unique_key)")
                                continue
                            
                            # Password handling
                            if use_custom_passwords:
                                if not custom_password:
                                    error_count += 1
                                    errors.append(f"Row {index + 1}: Custom password required but not provided")
                                    continue
                                password = custom_password
                            else:
                                password = default_password
                            
                            # Check if unique_key already exists
                            if Voter.objects.filter(unique_key=unique_key).exists():
                                error_count += 1
                                errors.append(f"Row {index + 1}: Voter with unique key '{unique_key}' already exists")
                                continue
                            
                            # Check if username already exists
                            if User.objects.filter(username=username).exists():
                                user = User.objects.get(username=username)
                                # Update user information
                                user.email = email
                                user.set_password(password)  # Update password
                                user.save()
                            else:
                                # Create new user with hashed password
                                user = User.objects.create_user(
                                    username=username,
                                    email=email,
                                    password=password
                                )
                            
                            # Create or update voter
                            voter, created = Voter.objects.get_or_create(
                                election=election,
                                user=user,
                                defaults={'unique_key': unique_key}
                            )
                            
                            if not created:
                                # Update unique_key if voter already exists
                                voter.unique_key = unique_key
                                voter.save()
                            
                            success_count += 1
                            
                        except Exception as e:
                            error_count += 1
                            errors.append(f"Row {index + 1}: {str(e)}")
                            continue
                
                # Prepare result message
                if success_count > 0:
                    password_source = "custom passwords" if use_custom_passwords else "default password"
                    messages.success(
                        request, 
                        f"Successfully uploaded {success_count} voters to {election.title} using {password_source}"
                    )
                if error_count > 0:
                    messages.warning(request, f"Failed to upload {error_count} voters. Check the errors below.")
                    request.session['upload_errors'] = errors[:10]
                
            except json.JSONDecodeError:
                messages.error(request, "Invalid JSON file format")
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
            
            return redirect('upload_voters')
    
    else:
        form = VoterUploadForm()
    
    # Get errors from session if any
    errors = request.session.pop('upload_errors', [])
    
    return render(request, 'voting/upload_voters.html', {
        'form': form,
        'errors': errors
    })