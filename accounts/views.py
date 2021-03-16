from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse


def signup(request):
    """
    Signup view implementation : either register is successful and redirect to the login view, or render the form html.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("accounts:login"))
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {"form": form})
