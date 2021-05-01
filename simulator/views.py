from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import HouseguestSerializer

from .models import Houseguest


@api_view(['GET'])
def get_all_houseguests(request, *args, **kwargs):
    hlist = Houseguest.objects.all()
    houseguests = [x.serialize() for x in hlist]

    data = {
        "response": houseguests
    }

    return Response(data)
