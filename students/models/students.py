from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Student(models.Model):
    '''Student model'''

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta(object):
        verbose_name = _(u'Student')
        verbose_name_plural = _(u'Students')

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"First Name"))

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Last Name"))

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u"Patronymic"))

    birthday = models.DateField(
        blank=False,
        verbose_name=_(u"Date of birth"),
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=_(u"Photo"),
        null=True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Ticket"))

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Additional notes"))

    student_group = models.ForeignKey('Group',
                                      verbose_name=_(u"Group"),
                                      blank=False,
                                      null=True,
                                      on_delete=models.PROTECT)
