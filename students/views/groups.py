# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

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
