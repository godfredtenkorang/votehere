# voting/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Voter

User = get_user_model()

class VoterAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Check if this is a voter and hasn't voted yet
                voter = Voter.objects.get(user=user)
                if not voter.has_voted:
                    return user
        except (User.DoesNotExist, Voter.DoesNotExist):
            return None
        return None