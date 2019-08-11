from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from datetime import datetime

from ..models.students import Student
from ..models.groups import Group
from ..util import paginate, get_current_group


def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order student Listing
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    # paginate students
    context = paginate(students, 5, request, {}, var_name='students')
    return render(request, 'students/students_list.html', context)


@login_required
def students_add(request):
    # was form posted:
    if request.method == "POST":
        # was form add button clicked:
        if request.POST.get("add_button") is not None:
            # TODO: validate input from user
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last name is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Date of birth is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(u"Enter the correct date format (e.g. 1984-12-30)")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Select a group")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Select the correct group")
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                extensions_list = ('.jpg', '.gif', '.png', '.svg')
                if len(photo.read()) > 2000000:
                    errors['photo'] = _(u'Image size should be less than 2 MB')
                elif not photo.name.endswith(extensions_list):
                    errors['photo'] = _(u'The image file extension must be: .jpg, .gif, .png, .svg')
                else:
                    data['photo'] = photo

            # save students
            if not errors:
                student = Student(**data)
                student.save()

                # redirect to student list
                return HttpResponseRedirect(u'%s?status_message=%s' %
                                            (reverse('students_list'),
                                             _(u'Student successfully added')))

            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to students_list page is cancel button was clicked
            return HttpResponseRedirect(
                u"%s?status_message=%s" % (reverse('students_list'),
                                           _(u"Student addition canceled!"))
                )

    else:
        # initial form rendered
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, ** kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
                                  Submit('add_button', _(u'Save'),
                                         css_class="btn btn-primary"),
                                  Submit('cancel_button', _(u'Cancel'),
                                         css_class="btn btn-link"),
                                  ))

    def clean_student_group(self):
        '''Check if student is a leader in any group.
        If yes then ensure it's the same as selected group.'''
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        ''' validate group and raise exception if the selected groupis
        different from the group where the student is a leader'''
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(_(u'The student is the head of another group'), code='invalid')
        '''if validation was succesfull we return value of field
        student_group from the method'''
        return self.cleaned_data['student_group']


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return (u'%s?status_message=%s' % (reverse('students_list'),
                _("Student successfully edited!")))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=%s' %
                                        (reverse('students_list'),
                                         ("Student Editing Canceled")))

        else:
            return super(StudentUpdateView, self).\
                post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return (u'%s?status_message=%s' % (reverse('students_list'),
                _("Student successfully deleted!")))
