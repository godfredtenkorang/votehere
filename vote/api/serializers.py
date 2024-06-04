from rest_framework import serializers
from vote.models import Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'award', 'title', 'get_cat_image', 'date_added', 'end_date')