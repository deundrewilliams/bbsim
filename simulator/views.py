from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import GameSerializer
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from .models import Game, Contestant

# USER AUTHENTICATION
@api_view(['POST'])
def login_user(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"success": True})
    else:
        return Response({"success": False, "error": "Invalid Username/Password combination"}, status=400)

@api_view(['POST'])
def signup_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"success": False, "error": "Missing credentials"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"success": False, "error": "Email already exists"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"success": False, "error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)

        sim_user = Group.objects.get(name='Simulator User')

        user.groups.add(sim_user)

        login(request, user)

        return Response({"success": True})
    except Exception as e:
        return Response({"success": False, "error": e}, status=400)

@api_view(["POST"])
def logout_user(request):

    try:
        logout(request)
        return Response({"success": True})

    except Exception as e:
        return Response({"success": False, "error": e}, status=400)

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
    except Exception as e:
        print(e)
        print(f"Could not find contestant with name {requested_name}")
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

    if request.user.is_authenticated:

        data = dict(request.data)

        new_g = Game(user=request.user)
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

    else:

        return Response({"User is not authenticated"}, status=400)


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


@api_view(["GET"])
def home(request, *args, **kwargs):

    if request.user.is_authenticated:

        try:
            data = {}

            data["games"] = [x.serialize() for x in Game.objects.filter(user=request.user)]
            data["username"] = request.user.username

            return Response(data, content_type="application/javascript", status=200)

        except Exception as e:
            return Response({"error": e}, status=400)

    else:
        return Response({"error": "User not authenticated"}, status=400)
