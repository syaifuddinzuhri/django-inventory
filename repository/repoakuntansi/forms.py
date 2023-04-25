from repoakuntansi.models import User
from repoakuntansi.models import Jurnal
from repoakuntansi.models import TugasAkhir
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'password',
            'username',
            'email',
            'nama',
            'nim',
            'kelas',
            'kode_prodi',
            'tipe',
            'nip'
        ]


class JurnalForm(ModelForm):
    class Meta:
        model = Jurnal
        fields = "__all__"


class TugasAkhirForm(ModelForm):
    class Meta:
        model = TugasAkhir
        fields = "__all__"


class JurnalForm(ModelForm):
    class Meta:
        model = Jurnal
        fields = "__all__"
