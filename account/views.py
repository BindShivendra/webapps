import logging
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
        FormView,
        CreateView,
        UpdateView,
        DeleteView
    )   
from django.shortcuts import render
from django.urls import reverse_lazy

from account import models, forms

logger = logging.getLogger(__name__)

class SignUpView(FormView):
    template_name = 'account/signup.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to  = self.request.GET.get('next', '/')
        return redirect_to

    def form_valid(self, form):
        res = super().form_valid(form)
        form.save()
        
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        logger.info(f'New sign up for {email} view SignUpView')

        user = authenticate(email=email, password=password)
        login(self.request, user)

        form.send_email()
        messages.info(self.request, 'You signed up successfully.')

        return res

signup = SignUpView.as_view()
