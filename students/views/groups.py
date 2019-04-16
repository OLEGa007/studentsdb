# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group

def groups_list(request):
	groups = Group.objects.all()

	#try to order group Listing
	order_by = request.GET.get('order_by', '')
	if order_by in ('title', 'leader'):
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()
	else:
		groups = groups.order_by('title')

	# paginate groups
	paginator = Paginator(groups, 2)
	page = request.GET.get('page')
	try:
		groups = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer delivers first page
		groups = paginator.page(1)
	except EmptyPage:
		# If page is out or page range (e.g. 9999) delivers the last page
		groups = paginator.page(paginator.last_page)

	return render(request, 'students/groups_list.html', {'groups' : groups})

def groups_add(request):
	return HttpResponse('groups add form')

def groups_edit(request, gid):
	return HttpResponse('group %s edit form' % gid)

def groups_delete(request, gid):
	return HttpResponse('group %s delete form' % gid)
