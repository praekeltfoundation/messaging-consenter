from datetime import date
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from .forms import ConsentForm


class TestConsentView(TestCase):
    def test_uuid_is_added_to_inital_form(self):
        response = self.client.get("/consent/some-uuid/")

        self.assertContains(
            response,
            '<input type="hidden" name="uuid" value="some-uuid" id="id_uuid">',
            status_code=200,
        )

    @patch("consenter.forms.ConsentForm.save_consent")
    def test_form_submission_calls_save_consent(self, mock_save_consent):
        self.client.post(
            "/consent/some-uuid/", data={"checkbox": True, "uuid": "some-uuid"}
        )

        self.assertEqual(mock_save_consent.call_count, 1)

    @patch("consenter.forms.ConsentForm.save_consent")
    def test_form_submission_redirects_to_success(self, mock_save_consent):
        response = self.client.post(
            "/consent/some-uuid/", data={"checkbox": True, "uuid": "some-uuid"}
        )

        self.assertRedirects(
            response,
            "/consent/success/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class TestConsentForm(TestCase):
    @patch("temba_client.v2.TembaClient.create_flow_start", autospec=True)
    @patch("temba_client.v2.TembaClient.update_contact", autospec=True)
    @patch("temba_client.v2.TembaClient.get_contacts", autospec=True)
    def test_save_consent_calls_RP_to_update_contact(
        self, mock_get, mock_update, mock_flowstart
    ):
        # Build mock object
        mock_contact_object = Mock()
        mock_contact_object.uuid = "some-uuid"
        mock_contact_object.urns = ["tel:+27000000001"]
        mock_contact_object.fields = {
            "consent": None,
        }
        mock_get.return_value.first.return_value = mock_contact_object

        # Populate form
        form = ConsentForm(data={"checkbox": True, "uuid": "some-uuid"})
        form.is_valid()
        form.save_consent()

        # Check library calls
        self.assertEqual(mock_get.call_count, 1)
        call_args, call_kwargs = mock_get.call_args
        self.assertEqual(call_kwargs, {"uuid": "some-uuid"})
        self.assertEqual(mock_update.call_count, 1)
        call_args, call_kwargs = mock_update.call_args
        self.assertEqual(
            call_kwargs,
            {
                "contact": "some-uuid",
                "fields": {
                    "consent": "true",
                    "consent_date": "{}T00:00:00.000000+02:00".format(
                        date.today().isoformat()
                    ),
                },
            },
        )

        # confirm flowstart not called
        self.assertEqual(mock_flowstart.call_count, 0)

    @override_settings(RAPIDPRO_FLOW_ID="test-flow-id")
    @patch("temba_client.v2.TembaClient.create_flow_start", autospec=True)
    @patch("temba_client.v2.TembaClient.update_contact", autospec=True)
    @patch("temba_client.v2.TembaClient.get_contacts", autospec=True)
    def test_save_consent_starts_contact_on_flow(
        self, mock_get, mock_update, mock_flowstart
    ):
        # Build mock object
        mock_contact_object = Mock()
        mock_contact_object.uuid = "some-uuid"
        mock_get.return_value.first.return_value = mock_contact_object

        # Populate form
        form = ConsentForm(data={"checkbox": True, "uuid": "some-uuid"})
        form.is_valid()
        form.save_consent()

        # confirm flowstart called
        self.assertEqual(mock_flowstart.call_count, 1)
        call_args, call_kwargs = mock_flowstart.call_args
        self.assertEqual(
            call_kwargs, {"contacts": ["some-uuid"], "restart_participants": True}
        )
        self.assertIn("test-flow-id", call_args)

    @patch("temba_client.v2.TembaClient.update_contact", autospec=True)
    @patch("temba_client.v2.TembaClient.get_contacts", autospec=True)
    def test_save_consent_doesnt_update_nonexistent_contacts(
        self, mock_get, mock_update
    ):
        # Build mock object
        mock_get.return_value.first.return_value = None

        # Populate form
        form = ConsentForm(data={"checkbox": True, "uuid": "some-uuid"})
        form.is_valid()
        form.save_consent()

        # Check library calls
        self.assertEqual(mock_get.call_count, 1)
        call_args, call_kwargs = mock_get.call_args
        self.assertEqual(call_kwargs, {"uuid": "some-uuid"})
        self.assertEqual(mock_update.call_count, 0)
