# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models.monthjournal import MonthJournal
from ..models.students import Student
from ..util import paginate


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

        # calculate current, previouse and next month details
        # we need these data for month navigation element in the tmplate
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
            {'day': d, 'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days + 1)]

        # get all students from database
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
                            'present': journal and getattr(journal, 'present_\
                                                           day%d' % day,
                                                           False) or False,
                            'date': datetime(myear, mmonth,
                                             day).strftime('%Y-%m-%d'),
                            })

            # prepare metadata for current student
            students.append({
                            'fullname': u'%s %s' % (student.last_name,
                                                    student.first_name),
                            'days': days,
                            'id': student.id,
                            'udate_url': update_url,
                            })

        # apply pagination 10 students per page
        context = paginate(students, 10, self.request, context,
                           var_name='students')

        return context
