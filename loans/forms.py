from django import forms
from django.utils.translation import gettext_lazy as _


class AcceptLoanForm(forms.Form):
    contract = forms.FileField(
        help_text=_('Upload the creditor signed contract'),
        label=_('Contract')
    )
