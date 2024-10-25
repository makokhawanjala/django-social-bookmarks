from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, get_user_model, login
from .forms import LoginForm, UserRegistrationForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Contact, Profile
from .forms import (UserRegistrationForm, LoginForm, UserEditForm, ProfileEditForm)
from django.contrib import messages
from actions.utils import create_action
from actions.models import Action


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user instance but don't save it yet
            new_user = user_form.save(commit=False)
            # Set the password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user instance
            new_user.save()
            # Create a Profile instance for the new user
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            # Optionally, you can log the user in immediately after registration
        return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.POST.get('next') or request.GET.get('next')
                    if next_url:
                        # Redirect to the next URL if provided
                        return redirect(next_url)
                    else:
                        # Redirect to a default page, e.g., dashboard
                        return redirect('dashboard')                
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse("Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def edit(request):
    """Edit user profile view."""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Please correct the error below.')
            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})

User = get_user_model()
@login_required
def user_list(request):
    """List all users."""
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section':'people', 'users': users})

@login_required
def user_detail(request, username):
    """User detail view."""
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})

@require_POST
@login_required
def user_follow(request):
    """Follow or unfollow a user."""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user=User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


