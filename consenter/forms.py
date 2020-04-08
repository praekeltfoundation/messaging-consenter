from datetime import date

from django import forms
from django.conf import settings
from temba_client.v2 import TembaClient


class ConsentForm(forms.Form):
    checkbox = forms.BooleanField(label="I Accept the Terms", required=True)
    uuid = forms.CharField(widget=forms.HiddenInput(), required=True)

    def save_consent(self):
        # call RapidPro instance and save consent for uuid
        client = TembaClient(settings.RAPIDPRO_URL, settings.RAPIDPRO_TOKEN)
        contact = client.get_contacts(uuid=self.cleaned_data["uuid"]).first()
        if not contact:
            return

        client.update_contact(
            contact=self.cleaned_data["uuid"],
            fields={
                "consent_date": "{}T00:00:00.000000+02:00".format(
                    date.today().isoformat()
                ),
                "consent": "true",
            },
        )
