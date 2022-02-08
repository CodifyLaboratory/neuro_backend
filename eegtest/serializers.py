from django.db.models import Sum
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from user.serializers import UserListSerializer
from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, Calculation, \
    StimuliGroup, Operation, TestResultStimuli


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
        fields = ['id', 'title', 'description', 'status']


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


class OperationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
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


class StimuliGroupDetailSerializer(WritableNestedModelSerializer):
    calculation = serializers.PrimaryKeyRelatedField(read_only=True)
    stimuli = StimuliListSerializer(many=True, read_only=True)

    class Meta:
        model = StimuliGroup
        fields = ['id', 'calculation', 'stimuli']


class CalculationSerializer(WritableNestedModelSerializer):
    stimuli_groups = StimuliGroupSerializer(many=True, required=False)
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'operation', 'stimuli_groups']


class CalculationDetailSerializer(WritableNestedModelSerializer):
    stimuli_groups = StimuliGroupDetailSerializer(many=True, required=False)
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'operation', 'stimuli_groups']


class CalculationListSerializer(serializers.ModelSerializer):
    stimuli_groups = StimuliGroupListSerializer(many=True, read_only=True)
    test = TestListSerializer(many=False, read_only=True)
    parameter = ParameterListSerializer(many=False, read_only=True)
    operation = OperationListSerializer(many=False, read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'operation', 'stimuli_groups']


class TestResultStimuliListSerializer(serializers.ModelSerializer):
    # stimuli = StimuliListSerializer(many=False, read_only=True)
    stimuli = serializers.StringRelatedField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli', 'pow']


class TestResultStimuliSerializer(WritableNestedModelSerializer):
    test_result = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestResultStimuli
        fields = ['id', 'test_result', 'stimuli', 'pow']


class TestResultSerializer(WritableNestedModelSerializer):
    test_results_stimulus = TestResultStimuliSerializer(many=True, required=False)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'file', 'test_results_stimulus']
        read_only_fields = ['user', 'date']


class TestResultListSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status']
        read_only_fields = ['user', 'date']


class TestResultDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=False, read_only=True)
    test = serializers.StringRelatedField()
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)
    # test_results_stimulus = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = TestResult
        fields = ['user', 'description', 'test',  'title', 'description', 'status', 'test_results_stimulus']