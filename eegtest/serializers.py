from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Test, StimuliCategory, Stimuli

class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status']


class TestListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'title']


class StimuliCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StimuliCategory
        fields = ['id', 'title']


class StimuliSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimuli
        fields = ['id', 'order_id', 'test', 'category', 'title', 'description', 'duration', 'file']


class StimuliListSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimuli
        fields = ['id', 'order_id', 'test', 'category', 'title', 'description', 'duration', 'file']