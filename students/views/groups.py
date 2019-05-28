# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm, ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group
from ..models.students import Student
from ..util import paginate


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

    context = paginate(groups, 2, request, {}, var_name='groups')
    return render(request, 'students/groups_list.html', context)


class GroupAddForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *arg, **kwargs):
        super(GroupAddForm, self).__init__(*arg, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form_horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))



class GroupAddView(CreateView):
    model = Group
    # fields = '__all__'
    template_name = 'students/groups_add.html'
    form_class = GroupAddForm

    def get_success_url(self):
        return u'%s?status_message=Групу успішно додано!'\
                                    % reverse('groups_list')

    def post(self, request, *arg, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Додавання\
                                        групи відмінно'
                                        % reverse('groups_list'))
        else:
            return super(GroupAddView, self).post(request, *arg, **kwargs)


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


def groups_delete(request, pk):
    group = Group.objects.filter(id=pk)
    students = Student.objects.filter(student_group=pk)
    if request.method == "POST":
        if request.POST.get('del_button') is not None:
            if len(students) > 0:
                return HttpResponseRedirect(u'%s?status_message=Групу не \
                                            можна видалити оскільки до неї\
                                             входять студенти'
                                            % reverse('groups_list'))
            else:
                group.delete()
                return HttpResponseRedirect(u'%s?status_message=Групу видалено'
                                            % reverse('groups_list'))
        else:
            return HttpResponseRedirect(u'%s?status_message=Видалення групи\
                                        відмінено' % reverse('groups_list'))
    else:
        return render(request, 'students/groups_delete.html',
                      {'group': group[0].title, 'students': students})
