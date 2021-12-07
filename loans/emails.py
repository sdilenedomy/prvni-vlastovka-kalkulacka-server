import re
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from prvni_vlastovka_kalkulacka_server import settings

from django.utils import translation


def get_translation_in(language, s):
    with translation.override(language):
        return translation.gettext(s)


def generate_email_content(template, context):
    html_content = render_to_string(template, context)
    plain_content = strip_tags(html_content)

    plain_content = re.sub(r" {2,}", "", plain_content)
    plain_content = re.sub(r"^(\n *){3,}", "", plain_content)
    plain_content = re.sub(r"(\n *){3,}", "\n", plain_content)

    return html_content, plain_content


def send_new_offer_email(offer):
    # send email to client
    html_content, plain_content = generate_email_content(f"emails/new_offer_client_{offer.lender_language}.html",
                                                         {"offer": offer})

    subject = get_translation_in(offer.lender_language,"Information about a direct loan to První Vlaštovka")

    send_mail(
        subject,
        plain_content,
        settings.EMAIL_FINANCE,
        [offer.contact_email],
        html_message=html_content
    )

    # send email to self
    html_content, plain_content = generate_email_content("emails/new_offer_self.html", {"offer": offer,
                                                                                        "timestamp": datetime.now()})

    send_mail(
        f"Nová půjčka z kalkulačky: {offer.amount} {offer.currency}",
        plain_content,
        settings.EMAIL_FINANCE,
        [settings.EMAIL_FINANCE],
        html_message=html_content
    )
