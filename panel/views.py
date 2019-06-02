from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


# Create your views here.
from panel.forms import SignUpForm


@login_required(login_url='/sign-in/')
def index(request: WSGIRequest):
    return render(request, 'panel/index.html', {})


def sign_up(request: WSGIRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # send_email(email, username, raw_password)
            return redirect('/')
        else:
            return render(request, 'panel/sign-up.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'panel/sign-up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not request.user.is_authenticated:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect('/sign-up/')
        return redirect('/')
    return render(request, 'panel/sign-in.html', {'form': AuthenticationForm()})


def sign_out(request):
    logout(request)
    return redirect('/')
