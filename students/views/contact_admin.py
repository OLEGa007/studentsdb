import logging

from django import forms
from django.core.mail import send_mail

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):
    from_email = forms.EmailField(label=_(u'Your Email Address'))

    subject = forms.CharField(label=_(u'The title of the letter'), max_length=128)

    message = forms.CharField(label=_(u'Text of the message'),
                              widget=forms.Textarea)

    def __init__(self, *args, **kwargs):

        # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', _(u'Send')))


class ContactAdmin(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    message = _(u'The message was sent successfully')

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, *args, **kwargs):
        return super(ContactAdmin, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('contact_admin'),
                                          _(u"The message was sent successfully"))

    def form_valid(self, form):
        # This method is called to validate data
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, from_email, [ADMIN_EMAIL])
        except Exception:
            message = _(u'An unexpected error occurred while sending the email. Please try this form later')
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            message = _(u'The message was sent successfully')

        return super(ContactAdmin, self).form_valid(form)
