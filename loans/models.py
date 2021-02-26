from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _, ngettext_lazy, gettext


class Loan(models.Model):
    amount = models.IntegerField(verbose_name=_("Loan amount"))

    INTEREST_TYPE_OPTIONS = [
        ('one-time', _('one-time interest')),
        ('yearly', _('yearly interest'))
    ]
    interest_type = models.CharField(
        choices=INTEREST_TYPE_OPTIONS,
        max_length=10,
        verbose_name=_('interest type')
    )

    INTEREST_OPTIONS = [0, 0.5, 1, 1.5, 2, 2.5, 3]
    interest = models.FloatField(
        choices=map(lambda i: (i, f"{str(i)}%"), INTEREST_OPTIONS),
        verbose_name=_('interest')
    )

    DURATION_OPTIONS = [1, 2, 5, 10]
    DURATION_STRING = ngettext_lazy(
        '%d year',
        '%d years',
    )
    duration = models.IntegerField(
        choices=map(lambda i, dur_str=DURATION_STRING: (i, dur_str % i), DURATION_OPTIONS),
        verbose_name=_('duration')
    )

    contact_email = models.EmailField(verbose_name=_("contact email"))

    def __str__(self):
        return f'#{self.pk:05d}'


class LoanOffer(Loan):
    responsible_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('responsible person'),
        null=True
    )

    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')
        permissions = [
            ("accept_loanoffer", "Can accept the offer"),
        ]


class AcceptedLoan(Loan):
    contract = models.FileField(verbose_name=_('contract'), upload_to='contracts')

    class Meta:
        verbose_name = _('accepted loan')
        verbose_name_plural = _('accepted loans')
