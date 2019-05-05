# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm, ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group
from ..models.students import Student


def groups_list(request):
    groups = Group.objects.all()

    # try to order group Listing
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
        # If page is not an integer delivers first page
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out or page range (e.g. 9999) delivers the last page
        groups = paginator.page(paginator.last_page)

    return render(request, 'students/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('groups add form')


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form fields properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))

    def clean_leader(self):
        '''Check if the selected leader is not a member of other groups.'''
        # get students who is members of the group
        students = Student.objects.filter(student_group=self.instance)
        # validate if the leader is a member of current group
        if self.cleaned_data['leader'] not in students:
            raise ValidationError(
                u'Студент є членом іншої групи', code='invalid')
        '''if validation was succesfull we return value of field student_group
            from the method'''
        return self.cleaned_data['leader']


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return(u'%s?status_message=Групу успішно редаговано!' %
               reverse('groups_list'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Редагування групи\
                                        відмінено!' % reverse('groups_list'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDeleteForm(ModelForm):
    model = Group
    fields = '__all__'

    def clean_leader(self):
        '''Check if the group has members.'''
        # get students of the group
        students = Group.objects.filter(student_group=self.instance)
        print(students)
        if students is not None:
            raise ValidationError(u'Групу не можна видалити, тому що до неї\
                                  входять наступні студенти: %s'
                                  % (students), code='invalid')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'
    form = GroupDeleteForm

    # def get_success_url(self):
    #   return u'%s?status_message=Групу успішно видалено!' % reverse('groups_list')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Видалення групи\
                                        відмінено!' % reverse('groups_list'))
        else:
            return super(GroupDeleteView, self).post(request, *args, **kwargs)
