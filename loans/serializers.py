from rest_framework import serializers

from loans.models import LoanOffer


class LoanOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = '__all__'
