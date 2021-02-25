from django.views.generic.edit import FormView
from main import forms

# Create your views here.
class ContactUsView(FormView):
    template_name = 'contact_us.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form)

