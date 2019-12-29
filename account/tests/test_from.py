from django.test import TestCase
from django.core import mail

from account import forms

class TestForms(TestCase):
    
    def test_form_valid_sent_email(self):
        form = forms.UserCreationForm(
            {
                'email': 'user@email.com',
                'password1': 'Admin@123',
                'password2': 'Admin@123'
            }
        )
        self.assertTrue(form.is_valid())

        with self.assertLogs('account.forms', level='INFO') as log:
            form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to BookShop')
        self.assertGreaterEqual(len(log.output), 1)
        

