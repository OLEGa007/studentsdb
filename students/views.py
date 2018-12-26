# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Views for students

def students_list(request):
	students = (
		{'id': 1,
		 'first_name': u'Віталій',
		 'last_name': u'Подоба',
		 'ticket': 235,
		 'image': 'static/img/student.jpg'},
		{'id': 2,
		 'first_name': u'Андрій',
		 'last_name': u'Корост',
		 'ticket': 2123,
		 'image': 'static/img/student2.jpg'},
		{'id': 3,
		 'first_name': u'Тарас',
		 'last_name': u'Притула',
		 'ticket': 5332,
		 'image': 'static/img/student3.jpg'},
	)
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('Here we will have add student page	')

def students_edit(request, sid):
	return HttpResponse('student %s edit form' % sid)

def students_delete(request, sid):
	return HttpResponse('student %s delete form' % sid)

# Views for groups

def groups_list(request):
	groups = (
		{'id' : 1,
		 'name' : u'МтМ-21',
		 'head' : u'Ячменев Олег'},
		{'id' : 2,
		 'name' : u'МтМ-22',
		 'head' : u'Віталій Подоба'},
		{'id' : 3,
		 'name' : u'МтМ-23',
		 'head' : u'Іванов Андрій'},
	)
	return render(request, 'students/groups_list.html', {'groups' : groups})

def groups_add(request):
	return HttpResponse('groups add form')

def groups_edit(request, gid):
	return HttpResponse('group %s edit form' % gid)

def groups_delete(request, gid):
	return HttpResponse('group %s delete form' % gid)

# Views for journal

def journal(request):
	return HttpResponse('journal')
