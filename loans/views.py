from django.contrib.auth.decorators import permission_required
from django.http import FileResponse, HttpResponseNotFound
from rest_framework import viewsets

from loans.models import LoanOffer
from loans.serializers import LoanOfferSerializer


@permission_required('loans.view_acceptedloan')
def serve_contract(request, filename):
    try:
        return FileResponse(streaming_content=open(f'media/contracts/{filename}', 'rb'), as_attachment=True)
    except FileNotFoundError:
        return HttpResponseNotFound


class ApiLoanOfferViewSet(viewsets.ModelViewSet):
    queryset = LoanOffer.objects.all()
    serializer_class = LoanOfferSerializer
    http_method_names = ['options', 'post']
