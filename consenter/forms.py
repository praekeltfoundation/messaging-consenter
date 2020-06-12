import logging
from datetime import date, datetime

from django import forms
from django.conf import settings
from temba_client.v2 import TembaClient


class ConsentForm(forms.Form):
    checkbox = forms.BooleanField(label="I Accept the Terms", required=True)
    uuid = forms.CharField(widget=forms.HiddenInput(), required=True)

    def save_consent(self):
        # call RapidPro instance and save consent for uuid
        client = TembaClient(settings.RAPIDPRO_URL, settings.RAPIDPRO_TOKEN)
        logging.info('{} - Calling {} to get contact {}'.format(datetime.now().isoformat(), settings.RAPIDPRO_URL, self.cleaned_data["uuid"]))
        contact = client.get_contacts(uuid=self.cleaned_data["uuid"]).first()
        logging.info('{} - Completed call to get contact {}'.format(datetime.now().isoformat(), self.cleaned_data["uuid"]))

        if not contact:
            logging.info('{} - Contact {} not found. Exiting.'.format(datetime.now().isoformat(), self.cleaned_data["uuid"]))
            return

        contact_uuid = self.cleaned_data["uuid"]

        logging.info('{} - Calling {} to update fields for contact {}'.format(datetime.now().isoformat(), settings.RAPIDPRO_URL, self.cleaned_data["uuid"]))
        client.update_contact(
            contact=contact_uuid,
            fields={
                "consent_date": "{}T00:00:00.000000+02:00".format(
                    date.today().isoformat()
                ),
                "consent": "true",
            },
        )
        logging.info('{} - Completed call to update fields for contact {}'.format(datetime.now().isoformat(), self.cleaned_data["uuid"]))

        # Start the contact on a flow if one is specified
        if settings.RAPIDPRO_FLOW_ID:
            logging.info('{} - Calling {} to start contact {} on flow'.format(datetime.now().isoformat(), settings.RAPIDPRO_URL, self.cleaned_data["uuid"]))
            client.create_flow_start(
                settings.RAPIDPRO_FLOW_ID,
                contacts=[contact_uuid],
                restart_participants=True,
            )
            logging.info('{} - Completed call to start contact {} on flow'.format(datetime.now().isoformat(), self.cleaned_data["uuid"]))

        logging.info('{} - Exiting.'.format(datetime.now().isoformat()))
