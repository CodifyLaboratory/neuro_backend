from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Test, StimuliCategory, Stimuli


class StimuliCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StimuliCategory
        fields = ['id', 'title']


class StimuliListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    category = StimuliCategorySerializer(many=False, read_only=True)
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimuli
        fields = ['id', 'index', 'test', 'category', 'title', 'description', 'duration', 'file']


class StimuliSerializer(WritableNestedModelSerializer):
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimuli
        fields = ['id', 'index', 'test', 'category', 'title', 'description', 'duration', 'file']


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status']


class TestListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'title']


class TestDetailSerializer(serializers.ModelSerializer):
    stimulus = StimuliListSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'stimulus']


class TestDetailUpdateSerializer(WritableNestedModelSerializer):
    stimulus = StimuliSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status', 'stimulus']


class StimuliDetailSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimuli
        fields = ['id', 'index', 'test', 'category', 'title', 'description', 'duration', 'file']