from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import GameSerializer

from .models import Game, Contestant

# CONTESTANTS
@api_view(["POST"])
def create_contestant(request, *args, **kwargs):

    data = dict(request.data)

    try:
        new_contestant = Contestant(name=data["name"])
        new_contestant.save()
        data = new_contestant.serialize()
        return Response(data, content_type="application/javascript")
    except Exception as e:
        return Response({f"Could not create contestant, received error: {e}"}, status=400)



@api_view(["GET"])
def get_all_contestants(request, *args, **kwargs):
    clist = Contestant.objects.all()
    contestants = [x.serialize() for x in clist]

    data = {"response": contestants}

    return Response(data, content_type="application/javascript")

@api_view(["GET"])
def get_contestant(request, *args, **kwargs):

    requested_name = kwargs["name"]

    try:
        obj = Contestant.objects.get(name=requested_name)
        contestant = obj.serialize()
        return Response(contestant, content_type="application/javascript")
    except Exception:
        return Response(
            {f"Cannot find contestant with name: {requested_name}"}, status=400
        )

# GAMES
@api_view(["GET"])
def get_single_game(request, *args, **kwargs):

    requested_id = kwargs["id"]

    try:

        obj = Game.objects.get(id=requested_id)

        game = obj.serialize()
        return Response(game, content_type="application/javascript")
    except Exception:
        return Response(
            {f"Unable to retrieve game with id: {requested_id}"}, status=400
        )


@api_view(["POST"])
def create_game(request, *args, **kwargs):

    data = dict(request.data)

    new_g = Game()
    new_g.save()

    for c_id in data["contestants"]:
        c_obj = Contestant.objects.get(id=c_id)

        if c_obj:
            _ = c_obj.create_houseguest_clone(game_obj=new_g)
        else:
            new_g.delete()
            return Response(
                {f"Unable to create houseguest from contestant id: {c_id}"}, status=400
            )

    new_g.setup_game()

    new_g.save()

    return Response(new_g.serialize(), content_type="application/javascript")


@api_view(["POST"])
def sim_game(request, *args, **kwargs):

    # print(request.__dict__)

    data = dict(request.data)

    if type(data["id"]) == list:
        game_id = int(data["id"][0])
    else:
        game_id = int(data["id"])

    try:
        obj = Game.objects.get(id=game_id)
        print("Advancing")
        info = obj.advance_step()
        obj.save()
        print("Finished advancing")
        if obj.completed == True:
            obj.delete()

        return Response(info, content_type="application/javascript")
    except Exception as e:
        return Response({f"Unable to run game: {e}"}, status=400)




@api_view(["GET"])
def get_relationships(request, *args, **kwargs):

    return Response({}, status=400)
