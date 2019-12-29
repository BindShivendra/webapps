from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from unittest.mock import patch


from account import forms, models

class TestPage(TestCase):

    def test_signup_page_loads_correclty(self):
        res = self.client.get(reverse('auth:signup'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/signup.html')
        self.assertContains(res, 'BookShop')
        self.assertIsInstance(res.context['form'], forms.UserCreationForm)

    def test_signup_page_submission_works(self):
        data = {
                'email':'user@email.com',
                'password1': 'Admin@123',
                'password2': 'Admin@123'
            }
        with patch.object(forms.UserCreationForm, 'send_email') as mock:
            res = self.client.post(reverse('auth:signup'), data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(models.User.objects.filter(email='user@email.com').exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        mock.assert_called_once()

    def test_list_view_return_only_users_address(self):
        user_1 = models.User.objects.create_user(
            "Sebulba@email.com", 'I_will_win'
        )
        user_2 = models.User.objects.create_user(
            'Maz_Kanata@email.com', 'i_see_youz'
        )

        models.Address.objects.create(
            user=user_1,
            name='Sebulba',
            address1='Boonta Eve Podrace',
            address2='Outer Rim',
            zip_code='123456',
            city='Tatooine',
            country='us'
        )
        models.Address.objects.create(
            user=user_2,
            name='Maz Kanata',
            address1='the castle',
            address2='galaxys Western Reaches',
            zip_code='654321',
            city='Takodana',
            country='us'
        )

        self.client.force_login(user_2)
        res = self.client.get(reverse('auth:address_list'))
        self.assertEqual(res.status_code, 200)
        addr_list = models.Address.objects.filter(user=user_2)
        self.assertEqual(list(res.context['object_list']), list(addr_list))


    def test_address_create_stores_user(self):
        user_1 = models.User.objects.create_user(
            "Sebulba@email.com", 'I_will_win'
        )
        address = {    
            'name':'Sebulba',
            'address1':'Boonta Eve Podrace',
            'address2':'Outer Rim',
            'zip_code':'123456',
            'city':'Tatooine',
            'country':'us'
        }

        self.client.force_login(user_1)
        res = self.client.post(reverse('auth:create'), address)

        self.assertTrue(models.Address.objects.filter(user=user_1).exists())