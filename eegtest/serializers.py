from django.db.models import Sum
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from user.serializers import UserListSerializer
from .models import Test, StimuliCategory, Stimulus, TestResult, CortexSessionModel, Parameter, Calculation, \
    StimuliGroup


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
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'seconds', 'file']

    def get_seconds(self, obj):
        return obj.duration.total_seconds()


class StimuliSerializer(WritableNestedModelSerializer):
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'file']


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
        return Stimulus.objects.filter(test=obj.id).count()

    def get_total_duration(self, obj):
        return Stimulus.objects.filter(test=obj.id).aggregate(Sum('duration'))['duration__sum']


class TestDetailUpdateSerializer(WritableNestedModelSerializer):
    stimulus = StimuliSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status', 'stimulus']


class StimuliDetailSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'file']


class ParameterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'title']


class StimuliGroupListSerializer(serializers.ModelSerializer):
    calculation = serializers.PrimaryKeyRelatedField(read_only=True)
    stimuli = StimuliListSerializer(many=True, read_only=True)

    class Meta:
        model = StimuliGroup
        fields = ['id', 'calculation', 'stimuli']


class StimuliGroupSerializer(WritableNestedModelSerializer):
    calculation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StimuliGroup
        fields = ['id', 'calculation', 'stimuli']


class CalculationSerializer(WritableNestedModelSerializer):
    stimuli_groups = StimuliGroupSerializer(many=True)
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'stimuli_groups']


class CalculationListSerializer(WritableNestedModelSerializer):
    stimuli_groups = StimuliGroupListSerializer(many=True, read_only=True)
    test = TestListSerializer(many=False, read_only=True)
    parameter = ParameterListSerializer(many=False, read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'stimuli_groups']


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


class HeadsetSerializer(serializers.Serializer):
    headset = serializers.CharField(max_length=200)

    def save(self):
        headset = self.validated_data['headset']
        return headset


class GetUserSerializer(serializers.Serializer):
    cortex_token = serializers.CharField(min_length=20)

    def save(self):
        cortex_token = self.validated_data['cortex_token']
        return cortex_token


class CreateSessionSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    cortex_token = serializers.CharField(min_length=20, read_only=True)
    headset = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status', 'cortex_token', 'headset']
        read_only_fields = ['user', 'date']


class CreateSession1Serializer(serializers.Serializer):
    cortex_token = serializers.CharField(min_length=20)
    headset = serializers.CharField(max_length=200)

    def save(self):
        cortex_token = self.validated_data['cortex_token']
        headset = self.validated_data['headset']
        return cortex_token, headset


class CloseSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(min_length=20)

    def save(self):
        session_id = self.validated_data['session_id']
        return session_id


class SubscribeDataSerializer(serializers.Serializer):
    cortex_token = serializers.CharField(min_length=20)
    session_id = serializers.CharField(min_length=20)

    def save(self):
        cortex_token = self.validated_data['cortex_token']
        session_id = self.validated_data['session_id']
        return cortex_token, session_id


class ExportRecordSerializer(serializers.Serializer):
    cortex_token = serializers.CharField(min_length=20)
    record_ids = serializers.CharField(min_length=20)
    folder = serializers.CharField(min_length=2)

    def save(self):
        cortex_token = self.validated_data['cortex_token']
        record_ids = self.validated_data['record_ids']
        folder = self.validated_data['folder']
        return cortex_token, record_ids, folder


class CortexClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CortexSessionModel
        fields = ['id', 'user', 'url']
