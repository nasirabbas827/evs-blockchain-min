# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth import login, logout
# from .models import Election

# def home(request):
#     return render(request, 'home.html')

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout
# from .models import Election, Candidate, Vote

# from hashlib import sha256
# from .blockchain import Block

# @login_required
# def election_detail(request, election_id):
#     election = get_object_or_404(Election, pk=election_id)
#     candidates = Candidate.objects.filter(election=election)

#     if request.method == 'POST':
#         selected_candidate_id = request.POST.get('selected_candidate')
#         selected_candidate = get_object_or_404(Candidate, pk=selected_candidate_id)

#         # Check if the user has already voted
#         existing_vote = Vote.objects.filter(user=request.user, election=election).first()
#         if existing_vote:
#             return redirect('election_detail', election_id=election_id)

#         # Create a new block and associate it with the user's vote
#         previous_block = Block.objects.order_by('-id').first()
#         block_data = f"{request.user.id}-{selected_candidate.id}-{election.id}"
#         block_hash = sha256(block_data.encode()).hexdigest()
#         new_block = Block.objects.create(hash_code=block_hash, previous_block=previous_block, data=block_data)

#         # Create a new vote and associate it with the user, selected candidate, and block
#         Vote.objects.create(user=request.user, election=election, candidate=selected_candidate, block=new_block)

#         return redirect('election_detail', election_id=election_id)

#     return render(request, 'election_detail.html', {'election': election, 'candidates': candidates})
# def custom_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def custom_logout(request):
#     logout(request)
#     return redirect('home')

# def custom_register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .models import Election, Candidate, Vote
from hashlib import sha256
from .blockchain import Blockchain , time , hashlib

from django.utils import timezone 

def home(request):
    return render(request, 'home.html')

@login_required
def election_list(request):
    elections = Election.objects.all()
    return render(request, 'election_list.html', {'elections': elections})

from .models import Block

# @login_required
# def election_detail(request, election_id):
#     election = get_object_or_404(Election, pk=election_id)
#     candidates = Candidate.objects.filter(election=election)
#     user_vote = Vote.objects.filter(user=request.user, election=election).first()

#     blockchain = Blockchain()  # Create a new blockchain instance

#     if request.method == 'POST':
#         selected_candidate_id = request.POST.get('selected_candidate')
#         selected_candidate = get_object_or_404(Candidate, pk=selected_candidate_id)

#         if user_vote:
#             return redirect('election_detail', election_id=election_id)

#         block_data = {
#             'user_id': request.user.id,
#             'username': request.user.username,
#             'candidate_id': selected_candidate.id,
#             'election_id': election.id,
#         }

#         new_block = blockchain.add_block(block_data, leading_zeros=4)

#         # Generate the hash_code using the block data
#         data_string = f"{block_data['username']}  has casted vote to {selected_candidate.name} in {election.name}"
#         hash_code = hashlib.sha256(data_string.encode()).hexdigest()

#         new_block_instance = Block.objects.create(
#             hash_code=hash_code,
#             nonce=new_block.nonce,
#             previous_block=None,  # Set as needed
#             data=data_string,  # Set the data
#         )

#         new_vote = Vote.objects.create(user=request.user, election=election, candidate=selected_candidate)
#         new_vote.block = new_block_instance
#         new_vote.save()

#         return render(request, 'election_detail.html', {'election': election, 'candidates': candidates, 'user_vote': new_vote})

#     return render(request, 'election_detail.html', {'election': election, 'candidates': candidates, 'user_vote': user_vote})

@login_required
def election_detail(request, election_id):
    election = get_object_or_404(Election, pk=election_id)

    if election.status != 'ongoing':
        return render(request, 'election_status.html', {'election': election})
    
    candidates = Candidate.objects.filter(election=election)
    user_vote = Vote.objects.filter(user=request.user, election=election).first()

    blockchain = Blockchain()  # Create a new blockchain instance

    if request.method == 'POST':
        selected_candidate_id = request.POST.get('selected_candidate')
        selected_candidate = get_object_or_404(Candidate, pk=selected_candidate_id)

        if user_vote:
            return redirect('election_detail', election_id=election_id)

        # Get the hash of the most recent block as the previous hash
        previous_block = Block.objects.order_by('-id').first()

        block_data = {
            'username': request.user.username,
            'candidate_id': selected_candidate.id,
            'election_id': election.id,
        }

        new_block = blockchain.add_block(block_data, leading_zeros=4)

        # Generate the hash_code using the block data
        data_string = f"{block_data['username']} has casted vote to {selected_candidate.name} in {election.name}"
        hash_code = hashlib.sha256(data_string.encode()).hexdigest()

        new_block_instance = Block.objects.create(
            hash_code=hash_code,
            nonce=new_block.nonce,
            previous_block=previous_block,  # Set the previous block
            data=data_string,
        )

        new_vote = Vote.objects.create(user=request.user, election=election, candidate=selected_candidate)
        new_vote.block = new_block_instance
        new_vote.save()

        return render(request, 'election_detail.html', {'election': election, 'candidates': candidates, 'user_vote': new_vote})

    return render(request, 'election_detail.html', {'election': election, 'candidates': candidates, 'user_vote': user_vote})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Election, Candidate, Vote

@login_required
def view_results(request, election_id):
    election = Election.objects.get(pk=election_id)
    
    # Check if the current user has cast a vote in this election
    user_vote = Vote.objects.filter(user=request.user, election=election).first()
    if not user_vote:
        return render(request, 'no_results.html', {'election': election})

    # Retrieve all the votes for this election and candidates
    candidates = Candidate.objects.filter(election=election)
    vote_counts = {}
    for candidate in candidates:
        votes_received = Vote.objects.filter(election=election, candidate=candidate).count()
        vote_counts[candidate] = votes_received
    
    # Find the winner
    winner = max(vote_counts, key=vote_counts.get)

    return render(request, 'view_results.html', {'election': election, 'winner': winner, 'vote_counts': vote_counts})


from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

