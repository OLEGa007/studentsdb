from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from ..models.monthjournal import MonthJournal
from ..models.students import Student
from ..util import paginate, get_current_group

import pdb


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(
                self.request.GET['month'], '%Y-%m-%d').date()
        else:
            # otherwise display current day and month
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details
        # we need these data for month navigation element in the template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['cur_month'] = month.strftime('%Y-%m-%d')
        context['month_verbose'] = month.strftime('%B')

        # prepare variable for header to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [
            {'day': d, 'verbose': day_abbr[weekday(myear, mmonth, d)][:3]}
            for d in range(1, number_of_days + 1)]
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        # get all students from database, of just one if we need to display
        # only one student
        if kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        elif current_group:
            queryset = Student.objects.filter(student_group=current_group).order_by('last_name')
        else:
            queryset = Student.objects.all().order_by('last_name')

        # url to update student presence, for form post
        update_url = reverse('journal')

        # go over all students and collect data about presence durin the month
        students = []
        for student in queryset:
            # try to get journal object by month the selected month and
            # thestudent
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence for current student
            days = []
            for day in range(1, number_of_days + 1):
                days.append({
                            'day': day,
                            'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                            'date': datetime(myear, mmonth,
                                             day).strftime('%Y-%m-%d'),
                            })

            # prepare metadata for current student
            students.append({
                            'fullname': u'%s %s' % (student.last_name,
                                                    student.first_name),
                            'days': days,
                            'id': student.id,
                            'update_url': update_url,
                            })

        # apply pagination 10 students per page
        context = paginate(students, 10, self.request, context,
                           var_name='students')

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student=student,
                                                     date=month)[0]

        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})
