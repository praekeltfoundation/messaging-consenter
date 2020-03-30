from datetime import date
from django.test import TestCase
from unittest.mock import Mock, patch

from .forms import ConsentForm


class TestConsentView(TestCase):
    def test_uuid_is_added_to_inital_form(self):
        response = self.client.get("/consent/some-uuid/")

        self.assertContains(
            response,
            '<input type="hidden" name="uuid" value="some-uuid" id="id_uuid">',
            status_code=200)
    
    @patch("consenter.forms.ConsentForm.save_consent")
    def test_form_submission_calls_save_consent(self, mock_save_consent):
        response = self.client.post(
            "/consent/some-uuid/",
            data={"checkbox": True, "uuid": "some-uuid"}
        )

        self.assertEqual(mock_save_consent.call_count, 1)
    

class TestConsentForm(TestCase):
    @patch("temba_client.v2.TembaClient.update_contact", autospec=True)
    @patch("temba_client.v2.TembaClient.get_contacts", autospec=True)
    def test_save_consent_calls_RP_to_update_contact(self, mock_get, mock_update):        
        # Build mock object
        mock_contact_object = Mock()
        mock_contact_object.uuid = "some-uuid"
        mock_contact_object.urns = ["tel:+27000000001"]
        mock_contact_object.fields = {"consent": None, }
        mock_get.return_value.first.return_value = mock_contact_object

        # Populate form
        form = ConsentForm(data = {"checkbox": True, "uuid": "some-uuid"})
        form.is_valid()
        form.save_consent()

        # Check library calls
        self.assertEqual(mock_get.call_count, 1)
        call_args, call_kwargs = mock_get.call_args
        self.assertEqual(call_kwargs, {"uuid": "some-uuid"})
        self.assertEqual(mock_update.call_count, 1)
        call_args, call_kwargs = mock_update.call_args
        self.assertEqual(call_kwargs, {
            "contact": "some-uuid",
            "fields": {
                "consent": "true",
                "consent_date": "{}T00:00:00.000000+02:00".format(
                    date.today().isoformat())
            }
        })

    @patch("temba_client.v2.TembaClient.update_contact", autospec=True)
    @patch("temba_client.v2.TembaClient.get_contacts", autospec=True)
    def test_save_consent_doesnt_update_nonexistent_contacts(self, mock_get, mock_update):        
        # Build mock object
        mock_get.return_value.first.return_value = None

        # Populate form
        form = ConsentForm(data = {"checkbox": True, "uuid": "some-uuid"})
        form.is_valid()
        form.save_consent()

        # Check library calls
        self.assertEqual(mock_get.call_count, 1)
        call_args, call_kwargs = mock_get.call_args
        self.assertEqual(call_kwargs, {"uuid": "some-uuid"})
        self.assertEqual(mock_update.call_count, 0)
