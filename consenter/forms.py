from datetime import date

import structlog
from django import forms
from django.conf import settings
from temba_client.v2 import TembaClient


class ConsentForm(forms.Form):
    checkbox = forms.BooleanField(label="I Accept the Terms", required=True)
    uuid = forms.CharField(widget=forms.HiddenInput(), required=True)

    def save_consent(self):
        # call RapidPro instance and save consent for uuid
        log = structlog.get_logger()
        client = TembaClient(settings.RAPIDPRO_URL, settings.RAPIDPRO_TOKEN)
        log.msg(
            "- Calling {} to get contact {}".format(
                settings.RAPIDPRO_URL, self.cleaned_data["uuid"]
            )
        )
        contact = client.get_contacts(uuid=self.cleaned_data["uuid"]).first()
        log.msg("- Completed call to get contact {}".format(self.cleaned_data["uuid"]))

        if not contact:
            log.msg(
                "- Contact {} not found. Exiting.".format(self.cleaned_data["uuid"])
            )
            return

        contact_uuid = self.cleaned_data["uuid"]

        log.msg(
            "- Calling {} to update fields for contact {}".format(
                settings.RAPIDPRO_URL, contact_uuid
            )
        )
        client.update_contact(
            contact=contact_uuid,
            fields={
                "consent_date": "{}T00:00:00.000000+02:00".format(
                    date.today().isoformat()
                ),
                "consent": "true",
            },
        )
        log.msg("- Completed call to update fields for contact {}".format(contact_uuid))

        # Start the contact on a flow if one is specified
        if settings.RAPIDPRO_FLOW_ID:
            log.msg(
                "- Calling {} to start contact {} on flow".format(
                    settings.RAPIDPRO_URL, contact_uuid
                )
            )
            client.create_flow_start(
                settings.RAPIDPRO_FLOW_ID,
                contacts=[contact_uuid],
                restart_participants=True,
            )
            log.msg("- Completed call to start contact {} on flow".format(contact_uuid))

        log.msg("- Exiting.")
