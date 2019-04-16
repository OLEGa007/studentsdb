# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
import os

from ..models.students import Student
from ..models.groups import Group

def students_list(request):
	students = Student.objects.all()

	#try to order student Listing
	order_by = request.GET.get('order_by', '')
	if order_by in ('id', 'last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('last_name')

	# paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer delivers first page
		students = paginator.page(1)
	except EmptyPage:
		# If page is out or page range (e.g. 9999) delivers the last page
		students = paginator.page(paginator.last_page)

	return render(request, 'students/students_list.html', {'students': students}, {order_by : "last_name"})

def students_add(request):
	# was form posted:
	if request.method == "POST":
		# was form add button clicked:
		if request.POST.get("add_button") is not None:
			# TODO: validate input from user
			errors = {}
			# validate student data will go here
			data= {'middle_name' : request.POST.get('middle_name'), 'notes' : request.POST.get('notes')}

			# validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов'язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу"
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коррекнту групу"
				else:
					data['student_group'] = groups[0]

			photo = request.FILES.get('photo')
			if photo:
				extensions_list = ('.jpg', '.gif', '.png', '.svg')
				if len(photo.read()) > 2000000:
					errors['photo'] = u'Розмір зображення повинен бути менше 2 Мб'
				elif not photo.name.endswith(extensions_list):
					errors['photo'] = u'Розширення файлу зображення повинно бути: .jpg, .gif, .png, .svg'
				else:
					data['photo'] = photo

			# save students
			if not errors:
				student = Student(**data)
				student.save()

				# redirect to student list
				return HttpResponseRedirect(u'%s?status_message=Студента успішно додано!' % reverse('students_list'))

			else:
				# render form with errors and previous user input
				return render(request, 'students/students_add.html', {'groups' : Group.objects.all().order_by('title'), 'errors' : errors})

		elif request.POST.get('cancel_button') is not None:
			# redirect to students_list page is cancel button was clicked
			return HttpResponseRedirect(u"%s?status_message=Додавання студента скасовано!" % reverse('students_list'))

	else:
		# initial form rendered
		return render(request, 'students/students_add.html', {'groups' : Group.objects.all().order_by('title')})

def students_edit(request, sid):
	return HttpResponse('student %s edit form' % sid)

def students_delete(request, sid):
	return HttpResponse('student %s delete form' % sid)
