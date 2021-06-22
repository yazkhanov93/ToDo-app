from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Tasks
from .forms import TaskForm


def sign_up(request):
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'sign_up.html', {'form': form})


def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
	return render(request, 'login.html', {})


def logout_page(request):
	logout(request)
	return redirect('/')


@login_required(login_url='login')
def tasks(request):
	search = request.GET.get('search', '')
	if search:
		task = Tasks.objects.filter(Q(name__icontains=search)|Q(content__icontains=search))
	else:
		task = Tasks.objects.filter(user=request.user)
	return render(request, 'home.html', {'task': task})


def detail(request, pk):
	task_detail = Tasks.objects.get(id=pk)
	return render(request, 'detail.html', {'task_detail': task_detail})


@login_required(login_url='login')
def add_task(request):
	form = TaskForm()
	user = User.objects.get(id=request.user.id)
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = user
			obj.save()
			return redirect('/')
	return render(request, 'form.html', {'form': form})


def edit_task(request, pk):
	task = Tasks.objects.get(id=pk)
	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'form.html', {'task': task, 'form': TaskForm(instance=task)})


def delete_task(request, pk):
	task = Tasks.objects.get(id=pk)
	task.delete()
	return redirect('/')
