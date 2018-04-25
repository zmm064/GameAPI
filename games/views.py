from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# use Response to replace HttpResponse and JSONResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from games.models import Game
from games.serializers import GameSerializer


class JSONResponse(HttpResponse):
    ''' 定义HttpResponse的子类，使之能接收字典 '''，
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)

@api_view(['GET', 'POST'])
@csrf_exempt
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)

    elif request.method == 'POST':
        # game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

    elif request.method == 'PUT':
        # game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(game, data=request.data)  # 这里同时传了两个参数
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
