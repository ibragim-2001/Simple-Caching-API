from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import ItemsSerializer
from .models import Items


class ItemsView(APIView):

    def get(self, request):
        try:
            items = Items.objects.all()
        except Exception as exception:
            return Response({'message': str(exception)})
        serializer = ItemsSerializer(items, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)