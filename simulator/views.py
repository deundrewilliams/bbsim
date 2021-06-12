from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import GameSerializer

from .models import Houseguest, Game, Contestant


# CONTESTANTS

@api_view(['GET'])
def get_all_contestants(request, *args, **kwargs):
    clist = Contestant.objects.all()
    contestants = [x.serialize() for x in clist]

    data = {
        "response": contestants
    }

    return Response(data, content_type='application/javascript')

# GAMES
@api_view(['GET'])
def get_single_game(request, *args, **kwargs):

    requested_id = kwargs["id"]

    try:

        obj = Game.objects.get(id=requested_id)

        game = obj.serialize()
        return Response(game, content_type='application/javascript')
    except:
        return Response({f"Unable to retrieve game with id: {requested_id}"}, status=400)

@api_view(['POST'])
def create_game(request, *args, **kwargs):

    data = dict(request.data)

    hgs = []

    new_g = Game()
    new_g.save()

    for c_id in data['contestants']:
        # print(f"Getting id of {c_id}")
        c_obj = Contestant.objects.get(id=c_id)

        if c_obj:
            _ = c_obj.create_houseguest_clone(game_obj=new_g)
        else:
            new_g.delete()
            return Response({f"Unable to create houseguest from contestant id: {c_id}"}, status=400)

        # if hg_obj:
        #     hgs.append(hg_obj)
        # else:
        #     return Response({}, status=400)

    return Response(new_g.serialize(), content_type='application/javascript')

@api_view(['POST'])
def sim_game(request, *args, **kwargs):

    # print(request.__dict__)

    data = dict(request.data)

    if (type(data["id"]) == list):
        game_id = int(data["id"][0])
    else:
        game_id = int(data["id"])


    try:
        obj = Game.objects.get(id=game_id)
        obj.run_game()
        obj.save()
    except:
        return Response({"Unable to run game"}, status=400)

    # print(obj.serialize())

    return Response(obj.serialize(), content_type='application/javascript')

@api_view(['GET'])
def get_relationshops(request, *args, **kwargs):

    return Response({}, status=400)
