from django.contrib.auth.models import User
from account.models import Profile

class EmailAuthBackend:
    """
    Custom authentication backend that allows users to log in using their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    #
    def get_user(self, user_id):
        """Retrieve a user by their ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
def create_profile(backend, user, *args, **kwargs):
    """
    Create a Profile instance for the user after social authentication.
    """
    Profile.objects.get_or_create(user=user)