from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from django.db.models import Sum
from .models import Test, StimuliCategory, Stimuli, TestResult
from user.serializers import UserListSerializer


class StimuliCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StimuliCategory
        fields = ['id', 'title']


class StimuliListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    category = StimuliCategorySerializer(many=False, read_only=True)
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    seconds = serializers.SerializerMethodField()

    class Meta:
        model = Stimuli
        fields = ['id', 'index', 'test', 'category', 'title', 'description', 'duration', 'seconds', 'file']

    def get_seconds(self, obj):
        return obj.duration.total_seconds()


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
    stimulus_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'stimulus_count', 'total_duration', 'stimulus']

    def get_stimulus_count(self, obj):
        return Stimuli.objects.filter(test=obj.id).count()

    def get_total_duration(self, obj):
        return Stimuli.objects.filter(test=obj.id).aggregate(Sum('duration'))['duration__sum']


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


class TestResultSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status']
        read_only_fields = ['user', 'date']


class TestResultDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=False, read_only=True)
    test = TestListSerializer(many=False, read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status']
        read_only_fields = ['user', 'date']