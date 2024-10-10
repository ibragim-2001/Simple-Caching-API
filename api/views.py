import json
import redis
from settings.settings import redis_client

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from .serializers import ItemsSerializer
from .models import Items


class ItemsView(APIView):

    def get(self, request):
        try:
            # search for data in the cache
            cached_items = redis_client.get('items')

            if cached_items:
                # deserialization in dict using loads
                items = json.loads(cached_items)
            else:
                items_queryset = Items.objects.all()
                serializer = ItemsSerializer(items_queryset, many=True)
                # serialization in json using dump
                redis_client.set('items', json.dumps(serializer.data), ex=60)

                items = serializer.data

            return Response({'items': items}, status=HTTP_200_OK)

        except (redis.RedisError, json.JSONDecodeError) as e:
            return Response({'error': {str(e)}}, status=HTTP_500_INTERNAL_SERVER_ERROR)