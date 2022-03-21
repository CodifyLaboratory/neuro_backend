from django.db.models import Sum, Count, Q, FloatField, F, ExpressionWrapper, Avg, Case, When, Value, IntegerField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from user.serializers import UserListSerializer, UserListExportSerializer
from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, Calculation, TestResultStimuli, \
    TestParameterResult


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
    # fa1_value = serializers.DecimalField(decimal_places=2, max_digits=6)
    fa1_value = serializers.FloatField(default=0.0)
    fa2_value = serializers.FloatField(default=0.0)
    coh_value = serializers.FloatField(default=0.0)
    tar_value = serializers.FloatField(default=0.0)

    class Meta:
        model = Stimulus
        fields = ['id', 'test', 'title', 'fa1_value', 'fa2_value', 'coh_value', 'tar_value']


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


class CalculationList1Serializer(serializers.ModelSerializer):
    """ Calculation List View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    parameter = ParameterListSerializer(many=False, read_only=True)
    test_value = serializers.FloatField(default=0.0)
    rest_value = serializers.FloatField(default=0.0)
    result_value = serializers.FloatField(default=0.0)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'test_value', 'rest_value', 'result_value']


class CalculationSerializer(WritableNestedModelSerializer):
    """ Calculation Create View """
    test = serializers.PrimaryKeyRelatedField(read_only=True)
    parameter = ParameterListSerializer(many=False, required=False)
    test_stimuli_group = StimuliList1Serializer(many=True, required=False)
    rest_stimuli_group = StimuliList1Serializer(many=True, required=False)

    class Meta:
        model = Calculation
        fields = ['id', 'test', 'parameter', 'test_stimuli_group', 'rest_stimuli_group']


class TestSerializer(WritableNestedModelSerializer):
    """ Test View """

    class Meta:
        model = Test
        fields = ['id', 'title']


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

    # fa1_value = serializers.SerializerMethodField()
    # value = serializers.SerializerMethodField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli', 'fa1', 'fa2', 'coh', 'tar']

    # def get_stimulus(self, obj):
    #     stimuli_result_queryset = TestResultStimuli.objects.values('stimuli')
    #     stimuli_queryset = Stimulus.objects.filter(id__in=stimuli_result_queryset).distinct()
    #     return StimuliListSerializer(stimuli_queryset, many=True).data

    # def get_fa1_value(self, obj):
    #     stimuli_result_queryset = TestResultStimuli.objects.values('stimuli')
    #     stimuli_queryset = Stimulus.objects.filter(id__in=stimuli_result_queryset).distinct()
    #     stimuli_result_queryset = TestResultStimuli.objects.values('fa1').annotate(fa1_sum=Sum('fa1'))
    #     return StimuliListSerializer(stimuli_queryset, many=True).data

    # def get_value(self, obj):
    #     stimuli_result_queryset = TestResultStimuli.objects.values('stimuli')
    #     # print(stimuli_result_queryset)
    #     stimuli_queryset = Stimulus.objects.filter(id__in=stimuli_result_queryset).distinct()
    #     return TestResultStimuli.objects.filter(stimuli__in=stimuli_queryset).aggregate(Sum('fa1'))['fa1__sum']


class TestResultStimuliDetailSerializer(serializers.ModelSerializer):
    """ Result of test List View """
    # stimuli = StimuliListSerializer(many=False, read_only=True)
    stimuli = serializers.StringRelatedField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli', 'pow', 'fa1', 'fa2', 'coh', 'tar']


class TestResultStimuliSerializer(WritableNestedModelSerializer):
    """ Result of test Stimuli Create View """
    test_result = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestResultStimuli
        fields = ['id', 'test_result', 'stimuli', 'pow']


class TestParameterResultSerializer(serializers.ModelSerializer):
    """ Result of test Parameter View """
    test_result = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestParameterResult
        fields = ['id', 'test_result', 'parameter', 'calculation', 'test_value', 'rest_value', 'result_value']


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

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status']
        read_only_fields = ['user', 'date']

    # def get_value(self, obj):
    #     try:
    #         return TestResultStimuli.objects.filter(test_result=obj.id).aggregate(Sum('fa1'))['fa1__sum']
    #     except:
    #         return 0


class TestResultDetailExportSerializer(serializers.ModelSerializer):
    """ Result of test Export View """
    user = UserListExportSerializer(many=False, read_only=True)
    test = serializers.StringRelatedField()
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)
    test_results_parameters = TestParameterResultSerializer(many=True, read_only=True)

    class Meta:
        model = TestResult
        fields = ['user', 'description', 'test', 'title', 'description', 'status', 'test_results_stimulus',
                  'test_results_parameters']


class TestResultDetailSerializer(serializers.ModelSerializer):
    """ Result of test Detail View """
    user = UserListSerializer(many=False, read_only=True)
    test = TestListSerializer(many=False, read_only=True)
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)
    test_results_parameters = TestParameterResultSerializer(many=True, read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'date', 'title', 'description', 'file', 'status', 'test_results_stimulus',
                  'test_results_parameters']
        read_only_fields = ['user', 'date']


class TestResultDetailAdminSerializer(serializers.ModelSerializer):
    """ Result Detail for Admin View """
    user = serializers.StringRelatedField()
    test = serializers.StringRelatedField()
    test_results_stimuli = serializers.SerializerMethodField()
    test_results_parameters = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'test_results_stimuli', 'test_results_parameters', 'test_results_parameters']
        read_only_fields = ['user', 'date']

    def get_test_results_stimuli(self, obj):
        stimuli_result_queryset = TestResultStimuli.objects.values('stimuli').filter(test_result=obj.id)
        stimuli_queryset = Stimulus.objects.filter(id__in=stimuli_result_queryset,
                                                   test_results_stimulus__test_result=obj.id).annotate(
            fa1_value=Avg(F('test_results_stimulus__fa1')), fa2_value=Avg(F('test_results_stimulus__fa2')),
            coh_value=Avg(F('test_results_stimulus__coh')), tar_value=Avg(F('test_results_stimulus__tar')))
        return StimuliList1Serializer(stimuli_queryset, many=True).data

    def get_test_results_parameters(self, obj):
        # Test Value - FA1
        test_stimuli_group_fa1 = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=1)
        test_value_fa1 = Stimulus.objects.filter(id__in=test_stimuli_group_fa1, test_results_stimulus__test_result=obj.id).annotate(
            fa1_value=Avg(F('test_results_stimulus__fa1'), output_field=FloatField())).aggregate(Avg('fa1_value'))[
            'fa1_value__avg']

        # Test Value - FA2
        test_stimuli_group_fa2 = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=2)
        test_value_fa2 = Stimulus.objects.filter(id__in=test_stimuli_group_fa2, test_results_stimulus__test_result=obj.id).annotate(
            fa2_value=Avg(F('test_results_stimulus__fa2'), output_field=FloatField())).aggregate(Avg('fa2_value'))[
            'fa2_value__avg']

        # Test Value - COH
        test_stimuli_group_coh = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=3)
        test_value_coh = Stimulus.objects.filter(id__in=test_stimuli_group_coh, test_results_stimulus__test_result=obj.id).annotate(
            coh_value=Avg(F('test_results_stimulus__coh'), output_field=FloatField())).aggregate(Avg('coh_value'))[
            'coh_value__avg']

        # Test Value - TAR
        test_stimuli_group_tar = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=4)
        test_value_tar = Stimulus.objects.filter(id__in=test_stimuli_group_tar, test_results_stimulus__test_result=obj.id).annotate(
            tar_value=Avg(F('test_results_stimulus__tar'), output_field=FloatField())).aggregate(Avg('tar_value'))[
            'tar_value__avg']

        # Rest Value - FA1
        rest_stimuli_group_fa1 = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=1)
        rest_value_fa1 = Stimulus.objects.filter(id__in=rest_stimuli_group_fa1, test_results_stimulus__test_result=obj.id).annotate(
            fa1_value=Avg(F('test_results_stimulus__fa1'), output_field=FloatField())).aggregate(Avg('fa1_value'))[
            'fa1_value__avg']

        # Rest Value - FA2
        rest_stimuli_group_fa2 = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=2)
        rest_value_fa2 = Stimulus.objects.filter(id__in=rest_stimuli_group_fa2, test_results_stimulus__test_result=obj.id).annotate(
            fa2_value=Avg(F('test_results_stimulus__fa2'), output_field=FloatField())).aggregate(Avg('fa2_value'))[
            'fa2_value__avg']

        # Rest Value - COH
        rest_stimuli_group_coh = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=3)
        rest_value_coh = Stimulus.objects.filter(id__in=rest_stimuli_group_coh, test_results_stimulus__test_result=obj.id).annotate(
            coh_value=Avg(F('test_results_stimulus__coh'), output_field=FloatField())).aggregate(Avg('coh_value'))[
            'coh_value__avg']

        # Rest Value - TAR
        rest_stimuli_group_tar = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id, test=obj.test, parameter=4)
        rest_value_tar = Stimulus.objects.filter(id__in=rest_stimuli_group_tar, test_results_stimulus__test_result=obj.id).annotate(
            tar_value=Avg(F('test_results_stimulus__tar'), output_field=FloatField())).aggregate(Avg('tar_value'))[
            'tar_value__avg']

        parameters_result_queryset = Calculation.objects.filter(test=obj.test).annotate(
            test_value=Case(
                When(parameter=1, then=Value(test_value_fa1)),
                When(parameter=2, then=Value(test_value_fa2)),
                When(parameter=3, then=Value(test_value_coh)),
                When(parameter=4, then=Value(test_value_tar)),
                default=Value(0.0)
            ),
            rest_value=Case(
                When(parameter=1, then=Value(rest_value_fa1)),
                When(parameter=2, then=Value(rest_value_fa2)),
                When(parameter=3, then=Value(rest_value_coh)),
                When(parameter=4, then=Value(rest_value_tar)),
                default=Value(0.0)
            ),
            result_value=Case(
                When(parameter=1, then=Value(test_value_fa1 - rest_value_fa1)),
                When(parameter=2, then=Value(test_value_fa2 - rest_value_fa2)),
                When(parameter=3, then=Value(test_value_coh - rest_value_coh)),
                When(parameter=4, then=Value(test_value_tar - rest_value_tar)),
                default=Value(0.0)
            ))

        return CalculationList1Serializer(parameters_result_queryset, many=True).data
