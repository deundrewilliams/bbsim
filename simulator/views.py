from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import GameSerializer

from .models import Houseguest, Game


# HOUSEGUESTS

@api_view(['GET'])
def get_all_houseguests(request, *args, **kwargs):
    hlist = Houseguest.objects.all()
    houseguests = [x.serialize() for x in hlist]

    data = {
        "response": houseguests
    }

    return Response(data)

# GAMES
@api_view(['GET'])
def get_single_game(request, *args, **kwargs):

    requested_id = kwargs["id"]

    try:

        obj = Game.objects.get(id=requested_id)

        game = obj.serialize()
        return Response(game)
    except:
        return Response({}, status=400)

@api_view(['POST'])
def create_game(request, *args, **kwargs):

    data = dict(request.data)

    hgs = []

    for hg_id in data['houseguests']:
        hg_obj = Houseguest.objects.get(id=hg_id)

        if hg_obj:
            hgs.append(hg_obj)
        else:
            return Response({}, status=400)

    try:
        new_g = Game()
        new_g.save()
        new_g.players.set(hgs)
    except:
        new_g.delete()
        return Response({}, status=400)

    return Response(new_g.serialize())

