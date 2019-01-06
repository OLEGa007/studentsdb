# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

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
