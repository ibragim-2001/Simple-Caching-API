import os
import json
import redis

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import ItemsSerializer
from .models import Items

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'))

class ItemsView(APIView):

    def get(self, request):
        try:
            cached_items = redis_client.get('items')

            if cached_items:
                items = json.loads(cached_items)
            else:
                items_queryset = Items.objects.all()
                serializer = ItemsSerializer(items_queryset, many=True)

                redis_client.set('items', json.dumps(serializer.data), ex=5)

                items = serializer.data

            return Response({'items': items}, status=HTTP_200_OK)

        except (redis.RedisError, json.JSONDecodeError) as e:
            return Response({'error': f'{str(e)}, An error occurred while fetching items.'}, status=500)