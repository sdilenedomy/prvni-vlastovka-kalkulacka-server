from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _, ngettext_lazy, gettext


class Loan(models.Model):
    amount = models.IntegerField(verbose_name=_("Loan amount"))

    CURRENCY_CHOICES = [
        ('Kč', 'Kč'),
        ('EUR', 'EUR')
    ]
    currency = models.CharField(
        max_length=3,
        verbose_name=_('currency'),
        choices=CURRENCY_CHOICES,
        default='Kč'
    )

    INTEREST_TYPE_OPTIONS = [
        ('end', _('repayment of both prinicipal and interest at the end')),
        ('yearly', _('yearly repayment of interest, principal at the end'))
    ]
    interest_type = models.CharField(
        choices=INTEREST_TYPE_OPTIONS,
        max_length=10,
        verbose_name=_('interest repayment type')
    )

    INTEREST_OPTIONS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    interest = models.FloatField(
        choices=map(lambda i: (i, f"{str(i)} %"), INTEREST_OPTIONS),
        verbose_name=_('interest')
    )

    DURATION_OPTIONS = list(range(1, 16))
    DURATION_STRING = ngettext_lazy(
        '%d year',
        '%d years',
    )
    duration = models.IntegerField(
        choices=map(lambda i, dur_str=DURATION_STRING: (i, dur_str % i), DURATION_OPTIONS),
        verbose_name=_('duration')
    )

    contact_email = models.EmailField(verbose_name=_("contact email"))

    LENDER_LANGUAGE_OPTIONS = settings.LANGUAGES
    lender_language = models.CharField(
        choices=LENDER_LANGUAGE_OPTIONS,
        max_length=2,
        verbose_name=_("lender language"),
        default="cs"
    )

    def __str__(self):
        return f'#{self.pk:05d}'


class LoanOffer(Loan):
    responsible_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('responsible person'),
        null=True,
        blank=True,
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
