from django.db.models import Sum
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from user.serializers import UserListSerializer, UserListExportSerializer
from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, Calculation, TestResultStimuli


class StimuliCategorySerializer(serializers.ModelSerializer):
    """ Stimuli Category View """
    class Meta:
        model = StimuliCategory
        fields = ['id', 'title']


class ParameterListSerializer(serializers.ModelSerializer):
    """ Parameter List View """
    class Meta:
        model = Parameter
        fields = ['id', 'title']


class StimuliListSerializer(serializers.ModelSerializer):
    """ Stimuli of test List View """
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    category = StimuliCategorySerializer(many=False, read_only=True)
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    seconds = serializers.SerializerMethodField()

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'seconds', 'file']

    def get_seconds(self, obj):
        return obj.duration.total_seconds()


class StimuliList1Serializer(serializers.ModelSerializer):
    """ Stimuli of test List View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'title']


class StimuliSerializer(WritableNestedModelSerializer):
    """ Stimuli Create view """
    id = serializers.ReadOnlyField(read_only=True, source='get_str_id')
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'file']


class CalculationListSerializer(serializers.ModelSerializer):
    """ Calculation List View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    parameter = ParameterListSerializer(many=False, read_only=True)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'test_stimuli_group', 'rest_stimuli_group']


class CalculationSerializer(WritableNestedModelSerializer):
    """ Calculation Create View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    parameter = ParameterListSerializer(many=False, read_only=True, required=False)
    test_stimuli_group = StimuliList1Serializer(many=True, required=False)
    rest_stimuli_group = StimuliList1Serializer(many=True, required=False)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'test_stimuli_group', 'rest_stimuli_group']


class TestSerializer(WritableNestedModelSerializer):
    """ Test View """

    class Meta:
        model = Test
        fields = ['id', 'title', 'calculations']


class TestCalculationSerializer(WritableNestedModelSerializer):
    """ Test View """
    calculations = CalculationSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'calculations']


class TestListSerializer(serializers.ModelSerializer):
    """ Test View """
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status']


class TestDetailSerializer(serializers.ModelSerializer):
    """ Test Detail View """
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
    """ Test Detail Update View """
    stimulus = StimuliSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'status', 'stimulus']


class StimuliDetailSerializer(serializers.ModelSerializer):
    """ Stimuli of test Detail View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'category', 'title', 'description', 'duration', 'file']


class TestResultStimuliListSerializer(serializers.ModelSerializer):
    """ Result of test List View """
    # stimuli = StimuliListSerializer(many=False, read_only=True)
    stimuli = serializers.StringRelatedField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli', 'pow', 'fa1', 'fa2', 'coh', 'tar']


class TestResultStimuliSerializer(WritableNestedModelSerializer):
    """ Result of test Create View """
    test_result = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestResultStimuli
        fields = ['id', 'test_result', 'stimuli', 'pow']


class TestResultSerializer(WritableNestedModelSerializer):
    """ Result of test Create View """
    test_results_stimulus = TestResultStimuliSerializer(many=True, required=False)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'file', 'test_results_stimulus', 'status', 'description', 'title']
        read_only_fields = ['user', 'date']


class TestResultListSerializer(serializers.ModelSerializer):
    """ Result of test List View """
    test = TestListSerializer(many=False, read_only=True)
    user = UserListSerializer(many=False, read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status', 'value']
        read_only_fields = ['user', 'date']

    def get_value(self, obj):
        try:
            return TestResultStimuli.objects.filter(test_result=obj.id).aggregate(Sum('fa1'))['fa1__sum']
        except:
            return 0


class TestResultDetailExportSerializer(serializers.ModelSerializer):
    """ Result of test Export View """
    user = UserListExportSerializer(many=False, read_only=True)
    test = serializers.StringRelatedField()
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)

    class Meta:
        model = TestResult
        fields = ['user', 'description', 'test', 'title', 'description', 'status', 'test_results_stimulus']


class TestResultDetailSerializer(serializers.ModelSerializer):
    """ Result of test Detail View """
    user = UserListSerializer(many=False, read_only=True)
    test = TestListSerializer(many=False, read_only=True)
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status', 'test_results_stimulus',
                  'value']
        read_only_fields = ['user', 'date']

    def get_value(self, obj):
        return TestResultStimuli.objects.filter(test_result=obj.id).aggregate(Sum('fa1'))['fa1__sum']
