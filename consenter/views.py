from django.conf import settings
from django.views.generic.edit import FormView

from .forms import ConsentForm


class ConsentView(FormView):
    template_name = "consenter/consent_form.html"
    form_class = ConsentForm
    success_url = settings.CONSENT_REDIRECT_URL

    def get_initial(self):
        """
        Populates the hidden uuid field in the form from the url.
        """
        initial = super().get_initial()
        initial["uuid"] = self.kwargs["user_uuid"]
        return initial

    def form_valid(self, form):
        """
        Calls the form save_consent method if the form is valid
        """
        form.save_consent()
        return super().form_valid(form)
