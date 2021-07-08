from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field

from .forms import AcceptLoanForm
from .models import LoanOffer, AcceptedLoan, Loan


class LoanResource(resources.ModelResource):
    interest = Field()

    def dehydrate_interest(self, loan):
        return loan.get_interest_display()

    class Meta:
        model = Loan
        exclude = ('loan_ptr',)


class LoanAdmin(admin.ModelAdmin):
    def amount_currency(self, obj):
        return f"{obj.amount} {obj.currency}"

    amount_currency.short_description = _('Loan amount')

    list_display = (
        '__str__',
        'amount_currency',
        'interest',
        'duration',
        'interest_type',
        'contact_email',
    )


# --- Accepted Loan ---

class AcceptedLoanResource(LoanResource):
    contract = Field()

    def dehydrate_contract(self, accepted_loan):
        return accepted_loan.contract.url

    class Meta:
        model = AcceptedLoan


class AcceptedLoanAdmin(ExportMixin, LoanAdmin):
    list_display = LoanAdmin.list_display + (
        'contract',
    )

    resource_class = AcceptedLoanResource


admin.site.register(AcceptedLoan, AcceptedLoanAdmin)


# --- Offer ---


class OfferResource(LoanResource):
    responsible_person = Field()

    def dehydrate_responsible_person(self, loan_offer):
        if loan_offer.responsible_person:
            return loan_offer.responsible_person.username
        else:
            return ""

    class Meta:
        model = LoanOffer


class OfferAdmin(ExportMixin, LoanAdmin):
    list_display_default = LoanAdmin.list_display

    def changelist_view(self, request, extra_context=None):
        if request.user.has_perm('loans.accept_loanoffer'):
            self.list_display = self.list_display_default + (
                'accept_button',
            )
        else:
            self.list_display = self.list_display_default
        return super(OfferAdmin, self).changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:offer_id>/accept/',
                 self.admin_site.admin_view(self.accept_loan),
                 name='accept'),
        ]
        return my_urls + urls

    def accept_button(self, obj):
        return format_html(
            '<a class="button" href="{}" style="text-decoration: none">{}</a>',
            reverse('admin:accept', args=[obj.pk]),
            _('Accept Offer')
        )

    accept_button.short_description = _('Offer Actions')

    def accept_loan(self, request, offer_id):
        if not request.user.has_perm('loans.accept_loanoffer'):
            raise PermissionDenied

        offer = LoanOffer.objects.get(pk=offer_id)

        if request.method == 'GET':
            form = AcceptLoanForm()
        elif request.method == 'POST':
            form = AcceptLoanForm(request.POST, request.FILES)
            if form.is_valid():
                accepted_loan = AcceptedLoan.objects.create(
                    amount=offer.amount,
                    interest_type=offer.interest_type,
                    interest=offer.interest,
                    duration=offer.duration,
                    contact_email=offer.contact_email,
                    contract=request.FILES['contract']
                )
                offer.delete()

                self.message_user(request, _('The contract was uploaded and the loan was moved to accepted loans.'))
                return HttpResponseRedirect(reverse('admin:loans_acceptedloan_change', args=[accepted_loan.pk]))
        else:
            return HttpResponse(status=405)

        context = self.admin_site.each_context(request)
        context['form'] = form
        context['opts'] = LoanOffer._meta
        context['title'] = _('Accept offer %s') % offer
        context['offer_name'] = offer
        context['offer_id'] = offer_id

        return TemplateResponse(
            request,
            'admin/loans/loanoffer/accept.html',
            context
        )

    resource_class = OfferResource


admin.site.register(LoanOffer, OfferAdmin)
