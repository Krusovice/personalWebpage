from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# View for the logged-in message
@login_required
def logged_in(request):
    return render(request, 'logged_in.html')