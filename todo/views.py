from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required           # Only if u login then you can go

# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    # Sign up
    if request.method == 'GET':
        # Display signup form
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    # Process Sign up
    else:
        # Create a new user object
        if request.POST['password1'] == request.POST['password2']:
            # Check if user already exist
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Insert into database
                user.save()
                # login
                login(request, user)
                # Send to login page
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})

        # Tell user passwords didn't match
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords didnt not match'})

def loginuser(request):
    # Sign up
    if request.method == 'GET':
        # Display signup form
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    # Process Sign up
    else:
        # Check correct username and pw
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password does not match.'})
        else:
            # login
            login(request, user)
            # Send to login page
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    # Must put this, if not the post-processing of google, will instantiate this and auto log-out
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    # createtodo
    if request.method == 'GET':
        # Display createtodo form
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    # Process createtodo
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user;
            newtodo.save()
            # Send to login page
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error': 'You typed too much characters.'})



@login_required
def currenttodos(request):
    # Filter according to user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) # Only want objects with empty datecompleted
    return render(request, 'todo/currenttodos.html', {'todos':todos})



@login_required
def completedtodos(request):
    # Filter according to user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # Only want objects with empty datecompleted
    return render(request, 'todo/completedtodos.html', {'todos':todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #user=request.user will authenticate whether this user got todo #4
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo) # instance=todo will tell them we are reusing same user
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error': 'You typed too much characters.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #request.user will authenticate whether this user got todo #4
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #request.user will authenticate whether this user got todo #4
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
