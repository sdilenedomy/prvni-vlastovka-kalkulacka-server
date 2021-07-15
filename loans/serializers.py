import requests
from django.conf import settings
from rest_framework import serializers

from loans.emails import send_new_offer_email
from loans.models import LoanOffer


class LoanOfferSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = LoanOffer
        exclude = ['responsible_person']

    def validate_token(self, value):
        hcaptcha_response = requests.post('https://hcaptcha.com/siteverify',
                                          data={
                                              'secret': settings.HCAPTCHA_SECRET_KEY,
                                              'response': value
                                          })
        if not hcaptcha_response.json()['success'] and not settings.DEBUG:
            raise serializers.ValidationError("hCaptcha error")
        return value

    def create(self, validated_data):
        if "token" in validated_data:
            del validated_data["token"]

        offer = LoanOffer.objects.create(**validated_data)
        send_new_offer_email(offer)

        return offer
