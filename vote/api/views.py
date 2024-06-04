from rest_framework.decorators import api_view
from vote.models import Category, SubCategory
from vote.api.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def category_view(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)