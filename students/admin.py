# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.contrib import admin

from .models.students import Student
from .models.groups import Group
from .models.monthjournal import MonthJournal


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is a leader in any group. If yes then ensure it's
            the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        # validate group and raise exception if the selected group is
        # different from the group where the student is a leader
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи',
                                  code='invalid')
        # if validation was succesfull we return value of field student_group
        # from the method
        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket',
                     'notes']
    form = StudentFormAdmin  # bound form class to the view class

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):
    def clean_leader(self):
        '''Check if the selected leader is not a member of other groups.'''
        # get students who is members of the group
        students = Student.objects.filter(student_group=self.instance)
        # validate if the leader is a member of current group
        if self.cleaned_data['leader'] not in students and self.cleaned_data['leader'] is not None:
            raise ValidationError(u'Студент є членом іншої групи',
                                  code='invalid')
        # if validation was succesfull we return value of field student_group
        # from the method
        return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'notes', 'leader__first_name',
                     'leader__last_name']
    form = GroupFormAdmin


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)
