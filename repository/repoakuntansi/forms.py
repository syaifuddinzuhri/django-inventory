from repoakuntansi.models import User
from repoakuntansi.models import Jurnal
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class JurnalForm(ModelForm):
    class Meta:
        model = Jurnal
        fields = "__all__"
