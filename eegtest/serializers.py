from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, Count, Q, FloatField, F, ExpressionWrapper, Avg, Case, When, Value, IntegerField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from user.serializers import UserListSerializer, UserListExportSerializer
from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, Calculation, TestResultStimuli
import numpy as np
from scipy import signal


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
    test_value = serializers.FloatField()
    rest_value = serializers.FloatField()
    result_value = serializers.FloatField()

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
    stimuli = serializers.StringRelatedField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli', 'fa1', 'fa2', 'coh', 'tar']


class TestResultStimuliDetailSerializer(serializers.ModelSerializer):
    """ Result of test List View """
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


class TestResultDetailExportSerializer(serializers.ModelSerializer):
    """ Result of test Export View by stimuli """
    stimuli = serializers.StringRelatedField()

    AF3_theta = serializers.SerializerMethodField()
    AF3_alpha = serializers.SerializerMethodField()
    AF3_betaL = serializers.SerializerMethodField()
    AF3_betaH = serializers.SerializerMethodField()
    AF3_gamma = serializers.SerializerMethodField()

    F7_theta = serializers.SerializerMethodField()
    F7_alpha = serializers.SerializerMethodField()
    F7_betaL = serializers.SerializerMethodField()
    F7_betaH = serializers.SerializerMethodField()
    F7_gamma = serializers.SerializerMethodField()

    F3_theta = serializers.SerializerMethodField()
    F3_alpha = serializers.SerializerMethodField()
    F3_betaL = serializers.SerializerMethodField()
    F3_betaH = serializers.SerializerMethodField()
    F3_gamma = serializers.SerializerMethodField()

    FC5_theta = serializers.SerializerMethodField()
    FC5_alpha = serializers.SerializerMethodField()
    FC5_betaL = serializers.SerializerMethodField()
    FC5_betaH = serializers.SerializerMethodField()
    FC5_gamma = serializers.SerializerMethodField()

    T7_theta = serializers.SerializerMethodField()
    T7_alpha = serializers.SerializerMethodField()
    T7_betaL = serializers.SerializerMethodField()
    T7_betaH = serializers.SerializerMethodField()
    T7_gamma = serializers.SerializerMethodField()

    P7_theta = serializers.SerializerMethodField()
    P7_alpha = serializers.SerializerMethodField()
    P7_betaL = serializers.SerializerMethodField()
    P7_betaH = serializers.SerializerMethodField()
    P7_gamma = serializers.SerializerMethodField()

    O1_theta = serializers.SerializerMethodField()
    O1_alpha = serializers.SerializerMethodField()
    O1_betaL = serializers.SerializerMethodField()
    O1_betaH = serializers.SerializerMethodField()
    O1_gamma = serializers.SerializerMethodField()

    O2_theta = serializers.SerializerMethodField()
    O2_alpha = serializers.SerializerMethodField()
    O2_betaL = serializers.SerializerMethodField()
    O2_betaH = serializers.SerializerMethodField()
    O2_gamma = serializers.SerializerMethodField()

    P8_theta = serializers.SerializerMethodField()
    P8_alpha = serializers.SerializerMethodField()
    P8_betaL = serializers.SerializerMethodField()
    P8_betaH = serializers.SerializerMethodField()
    P8_gamma = serializers.SerializerMethodField()

    T8_theta = serializers.SerializerMethodField()
    T8_alpha = serializers.SerializerMethodField()
    T8_betaL = serializers.SerializerMethodField()
    T8_betaH = serializers.SerializerMethodField()
    T8_gamma = serializers.SerializerMethodField()

    FC6_theta = serializers.SerializerMethodField()
    FC6_alpha = serializers.SerializerMethodField()
    FC6_betaL = serializers.SerializerMethodField()
    FC6_betaH = serializers.SerializerMethodField()
    FC6_gamma = serializers.SerializerMethodField()

    F4_theta = serializers.SerializerMethodField()
    F4_alpha = serializers.SerializerMethodField()
    F4_betaL = serializers.SerializerMethodField()
    F4_betaH = serializers.SerializerMethodField()
    F4_gamma = serializers.SerializerMethodField()

    F8_theta = serializers.SerializerMethodField()
    F8_alpha = serializers.SerializerMethodField()
    F8_betaL = serializers.SerializerMethodField()
    F8_betaH = serializers.SerializerMethodField()
    F8_gamma = serializers.SerializerMethodField()

    AF4_theta = serializers.SerializerMethodField()
    AF4_alpha = serializers.SerializerMethodField()
    AF4_betaL = serializers.SerializerMethodField()
    AF4_betaH = serializers.SerializerMethodField()
    AF4_gamma = serializers.SerializerMethodField()

    class Meta:
        model = TestResultStimuli
        fields = ['stimuli',
                  'AF3_theta', 'AF3_alpha', 'AF3_betaL', 'AF3_betaH', 'AF3_gamma',
                  'F7_theta', 'F7_alpha', 'F7_betaL', 'F7_betaH', 'F7_gamma',
                  'F3_theta', 'F3_alpha', 'F3_betaL', 'F3_betaH', 'F3_gamma',
                  'FC5_theta', 'FC5_alpha', 'FC5_betaL', 'FC5_betaH', 'FC5_gamma',
                  'T7_theta', 'T7_alpha', 'T7_betaL', 'T7_betaH', 'T7_gamma',
                  'P7_theta', 'P7_alpha', 'P7_betaL', 'P7_betaH', 'P7_gamma',
                  'O1_theta', 'O1_alpha', 'O1_betaL', 'O1_betaH', 'O1_gamma',
                  'O2_theta', 'O2_alpha', 'O2_betaL', 'O2_betaH', 'O2_gamma',
                  'P8_theta', 'P8_alpha', 'P8_betaL', 'P8_betaH', 'P8_gamma',
                  'T8_theta', 'T8_alpha', 'T8_betaL', 'T8_betaH', 'T8_gamma',
                  'FC6_theta', 'FC6_alpha', 'FC6_betaL', 'FC6_betaH', 'FC6_gamma',
                  'F4_theta', 'F4_alpha', 'F4_betaL', 'F4_betaH', 'F4_gamma',
                  'F8_theta', 'F8_alpha', 'F8_betaL', 'F8_betaH', 'F8_gamma',
                  'AF4_theta', 'AF4_alpha', 'AF4_betaL', 'AF4_betaH', 'AF4_gamma']

    def get_AF3_theta(self, obj):
        return obj.pow[0]

    def get_AF3_alpha(self, obj):
        return obj.pow[1]

    def get_AF3_betaL(self, obj):
        return obj.pow[2]

    def get_AF3_betaH(self, obj):
        return obj.pow[3]

    def get_AF3_gamma(self, obj):
        return obj.pow[4]

    def get_F7_theta(self, obj):
        return obj.pow[5]

    def get_F7_alpha(self, obj):
        return obj.pow[6]

    def get_F7_betaL(self, obj):
        return obj.pow[7]

    def get_F7_betaH(self, obj):
        return obj.pow[8]

    def get_F7_gamma(self, obj):
        return obj.pow[9]

    def get_F3_theta(self, obj):
        return obj.pow[10]

    def get_F3_alpha(self, obj):
        return obj.pow[11]

    def get_F3_betaL(self, obj):
        return obj.pow[12]

    def get_F3_betaH(self, obj):
        return obj.pow[13]

    def get_F3_gamma(self, obj):
        return obj.pow[14]

    def get_FC5_theta(self, obj):
        return obj.pow[15]

    def get_FC5_alpha(self, obj):
        return obj.pow[16]

    def get_FC5_betaL(self, obj):
        return obj.pow[17]

    def get_FC5_betaH(self, obj):
        return obj.pow[18]

    def get_FC5_gamma(self, obj):
        return obj.pow[19]

    def get_T7_theta(self, obj):
        return obj.pow[20]

    def get_T7_alpha(self, obj):
        return obj.pow[21]

    def get_T7_betaL(self, obj):
        return obj.pow[22]

    def get_T7_betaH(self, obj):
        return obj.pow[23]

    def get_T7_gamma(self, obj):
        return obj.pow[24]

    def get_P7_theta(self, obj):
        return obj.pow[25]

    def get_P7_alpha(self, obj):
        return obj.pow[26]

    def get_P7_betaL(self, obj):
        return obj.pow[27]

    def get_P7_betaH(self, obj):
        return obj.pow[28]

    def get_P7_gamma(self, obj):
        return obj.pow[29]

    def get_O1_theta(self, obj):
        return obj.pow[30]

    def get_O1_alpha(self, obj):
        return obj.pow[31]

    def get_O1_betaL(self, obj):
        return obj.pow[32]

    def get_O1_betaH(self, obj):
        return obj.pow[33]

    def get_O1_gamma(self, obj):
        return obj.pow[34]

    def get_O2_theta(self, obj):
        return obj.pow[35]

    def get_O2_alpha(self, obj):
        return obj.pow[36]

    def get_O2_betaL(self, obj):
        return obj.pow[37]

    def get_O2_betaH(self, obj):
        return obj.pow[38]

    def get_O2_gamma(self, obj):
        return obj.pow[39]

    def get_P8_theta(self, obj):
        return obj.pow[40]

    def get_P8_alpha(self, obj):
        return obj.pow[41]

    def get_P8_betaL(self, obj):
        return obj.pow[42]

    def get_P8_betaH(self, obj):
        return obj.pow[43]

    def get_P8_gamma(self, obj):
        return obj.pow[44]

    def get_T8_theta(self, obj):
        return obj.pow[45]

    def get_T8_alpha(self, obj):
        return obj.pow[46]

    def get_T8_betaL(self, obj):
        return obj.pow[47]

    def get_T8_betaH(self, obj):
        return obj.pow[48]

    def get_T8_gamma(self, obj):
        return obj.pow[49]

    def get_FC6_theta(self, obj):
        return obj.pow[50]

    def get_FC6_alpha(self, obj):
        return obj.pow[51]

    def get_FC6_betaL(self, obj):
        return obj.pow[52]

    def get_FC6_betaH(self, obj):
        return obj.pow[53]

    def get_FC6_gamma(self, obj):
        return obj.pow[54]

    def get_F4_theta(self, obj):
        return obj.pow[55]

    def get_F4_alpha(self, obj):
        return obj.pow[56]

    def get_F4_betaL(self, obj):
        return obj.pow[57]

    def get_F4_betaH(self, obj):
        return obj.pow[58]

    def get_F4_gamma(self, obj):
        return obj.pow[59]

    def get_F8_theta(self, obj):
        return obj.pow[60]

    def get_F8_alpha(self, obj):
        return obj.pow[61]

    def get_F8_betaL(self, obj):
        return obj.pow[62]

    def get_F8_betaH(self, obj):
        return obj.pow[63]

    def get_F8_gamma(self, obj):
        return obj.pow[64]

    def get_AF4_theta(self, obj):
        return obj.pow[65]

    def get_AF4_alpha(self, obj):
        return obj.pow[66]

    def get_AF4_betaL(self, obj):
        return obj.pow[67]

    def get_AF4_betaH(self, obj):
        return obj.pow[68]

    def get_AF4_gamma(self, obj):
        return obj.pow[69]


class TestResultDetailSerializer(serializers.ModelSerializer):
    """ Result of test Detail View """
    user = UserListSerializer(many=False, read_only=True)
    test = TestListSerializer(many=False, read_only=True)
    test_results_stimulus = TestResultStimuliListSerializer(many=True, read_only=True)

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

    @classmethod
    def _get_wave(cls, pows, ind):
        return [i[ind] for i in pows]

    @classmethod
    def _get_coh(cls, pows):
        WAVE1_INDEX = 67
        WAVE2_INDEX = 57
        WAVE3_INDEX = 62
        wave1 = cls._get_wave(pows, WAVE1_INDEX)
        wave2 = cls._get_wave(pows, WAVE2_INDEX)
        wave3 = cls._get_wave(pows, WAVE3_INDEX)

        c1 = signal.coherence(wave1, wave2)
        c2 = signal.coherence(wave1, wave3)
        c3 = signal.coherence(wave2, wave3)

        pc1 = np.nanmean(c1[1]) if np.any(np.isfinite(c1[1])) else 1
        pc2 = np.nanmean(c2[1]) if np.any(np.isfinite(c2[1])) else 1
        pc3 = np.nanmean(c3[1]) if np.any(np.isfinite(c3[1])) else 1

        return (pc1 + pc2 + pc3) / 3 * 100

    def get_test_results_stimuli(self, obj: TestResultStimuli):
        stimuli_result_queryset = TestResultStimuli.objects.values('stimuli').filter(test_result=obj.id)
        stimuli_queryset = Stimulus.objects.filter(id__in=stimuli_result_queryset,
                                                   test_results_stimulus__test_result=obj.id).annotate(
            fa1_value=Avg(F('test_results_stimulus__fa1')), fa2_value=Avg(F('test_results_stimulus__fa2')),
            tar_value=Avg(F('test_results_stimulus__tar')))

        pows = {}
        stimuli_cohs = {}
        test_dataset = TestResultStimuli.objects.filter(test_result__id=obj.id)
        for data_item in test_dataset:
            if data_item.stimuli.id not in pows:
                pows[data_item.stimuli.id] = list()
            pows[data_item.stimuli.id].append(data_item.pow)

        for k, v in pows.items():
            stimuli_cohs[k] = self._get_coh(v)

        mutable_serializer = StimuliList1Serializer(stimuli_queryset, many=True).data.copy()

        _m = list()

        for item in mutable_serializer:
            _item = item.copy()
            _item['coh_value'] = stimuli_cohs[item['id']]
            _m.append(_item)

        return _m

    def get_test_results_parameters(self, obj):

        # Test Value - FA1
        test_stimuli_group_fa1 = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=1)
        if Stimulus.objects.filter(id__in=test_stimuli_group_fa1).exists():
            test_value_fa1 = \
                Stimulus.objects.filter(id__in=test_stimuli_group_fa1,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    fa1_value=Avg(F('test_results_stimulus__fa1'), output_field=FloatField())).aggregate(
                    Avg('fa1_value'))[
                    'fa1_value__avg']
        else:
            test_value_fa1 = float(0)

        # Test Value - FA2
        test_stimuli_group_fa2 = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=2)
        if Stimulus.objects.filter(id__in=test_stimuli_group_fa2).exists():
            test_value_fa2 = \
                Stimulus.objects.filter(id__in=test_stimuli_group_fa2,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    fa2_value=Avg(F('test_results_stimulus__fa2'), output_field=FloatField())).aggregate(
                    Avg('fa2_value'))['fa2_value__avg']
        else:
            test_value_fa2 = float(0)

        # Test Value - COH
        test_stimuli_group_coh = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=3)
        if Stimulus.objects.filter(id__in=test_stimuli_group_coh).exists():
            wave1 = TestResultStimuli.objects.values_list('wave1', flat=True).filter(
                stimuli_id__in=test_stimuli_group_coh, test_result=obj.id)
            wave2 = TestResultStimuli.objects.values_list('wave2', flat=True).filter(
                stimuli_id__in=test_stimuli_group_coh, test_result=obj.id)
            wave3 = TestResultStimuli.objects.values_list('wave3', flat=True).filter(
                stimuli_id__in=test_stimuli_group_coh, test_result=obj.id)
            pc1 = np.nanmean(signal.coherence(wave1, wave2)[1]) if np.any(
                np.isfinite(signal.coherence(wave1, wave2)[1])) else 1
            pc2 = np.nanmean(signal.coherence(wave1, wave3)[1]) if np.any(
                np.isfinite(signal.coherence(wave1, wave3)[1])) else 1
            pc3 = np.nanmean(signal.coherence(wave2, wave3)[1]) if np.any(
                np.isfinite(signal.coherence(wave2, wave3)[1])) else 1
            pc = (pc1 + pc2 + pc3) / 3 * 100
            test_value_coh = pc
        else:
            test_value_coh = float(0)

        # Test Value - TAR
        test_stimuli_group_tar = Calculation.objects.values('test_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=4)
        if Stimulus.objects.filter(id__in=test_stimuli_group_tar).exists():
            test_value_tar = \
                Stimulus.objects.filter(id__in=test_stimuli_group_tar,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    tar_value=Avg(F('test_results_stimulus__tar'), output_field=FloatField())).aggregate(
                    Avg('tar_value'))[
                    'tar_value__avg']
        else:
            test_value_tar = float(0)

        # Rest Value - FA1
        rest_stimuli_group_fa1 = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=1)
        if Stimulus.objects.filter(id__in=rest_stimuli_group_fa1).exists():
            rest_value_fa1 = \
                Stimulus.objects.filter(id__in=rest_stimuli_group_fa1,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    fa1_value=Avg(F('test_results_stimulus__fa1'), output_field=FloatField())).aggregate(
                    Avg('fa1_value'))[
                    'fa1_value__avg']
        else:
            rest_value_fa1 = float(0)

        # Rest Value - FA2
        rest_stimuli_group_fa2 = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=2)
        if Stimulus.objects.filter(id__in=rest_stimuli_group_fa2).exists():
            rest_value_fa2 = \
                Stimulus.objects.filter(id__in=rest_stimuli_group_fa2,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    fa2_value=Avg(F('test_results_stimulus__fa2'), output_field=FloatField())).aggregate(
                    Avg('fa2_value'))[
                    'fa2_value__avg']
        else:
            rest_value_fa2 = float(0)

        # Rest Value - COH
        rest_stimuli_group_coh = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=3)
        if Stimulus.objects.filter(id__in=rest_stimuli_group_coh).exists():
            wave1 = TestResultStimuli.objects.values_list('wave1', flat=True).filter(
                stimuli_id__in=rest_stimuli_group_coh, test_result=obj.id)
            wave2 = TestResultStimuli.objects.values_list('wave2', flat=True).filter(
                stimuli_id__in=rest_stimuli_group_coh, test_result=obj.id)
            wave3 = TestResultStimuli.objects.values_list('wave3', flat=True).filter(
                stimuli_id__in=rest_stimuli_group_coh, test_result=obj.id)
            pc1 = np.nanmean(signal.coherence(wave1, wave2)[1]) if np.any(
                np.isfinite(signal.coherence(wave1, wave2)[1])) else 1
            pc2 = np.nanmean(signal.coherence(wave1, wave3)[1]) if np.any(
                np.isfinite(signal.coherence(wave1, wave3)[1])) else 1
            pc3 = np.nanmean(signal.coherence(wave2, wave3)[1]) if np.any(
                np.isfinite(signal.coherence(wave2, wave3)[1])) else 1
            pc = (pc1 + pc2 + pc3) / 3 * 100
            rest_value_coh = pc
        else:
            rest_value_coh = float(0)

        # Rest Value - TAR
        rest_stimuli_group_tar = Calculation.objects.values('rest_stimuli_group').filter(test__results=obj.id,
                                                                                         test=obj.test, parameter=4)
        if Stimulus.objects.filter(id__in=rest_stimuli_group_tar).exists():
            rest_value_tar = \
                Stimulus.objects.filter(id__in=rest_stimuli_group_tar,
                                        test_results_stimulus__test_result=obj.id).annotate(
                    tar_value=Avg(F('test_results_stimulus__tar'), output_field=FloatField())).aggregate(
                    Avg('tar_value'))[
                    'tar_value__avg']
        else:
            rest_value_tar = float(0)

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


class TestResultDetailAdminExportSerializer(serializers.ModelSerializer):
    """ Result Detail for Admin View """
    fa1_value = serializers.SerializerMethodField()
    fa2_value = serializers.SerializerMethodField()
    coh_value = serializers.SerializerMethodField()
    tar_value = serializers.SerializerMethodField()

    class Meta:
        model = Stimulus
        fields = ['title', 'fa1_value', 'fa2_value', 'coh_value', 'tar_value']

    def get_fa1_value(self, obj):
        test_result_id = self.context.get('view').kwargs['pk']
        stimuli = TestResultStimuli.objects.filter(test_result=test_result_id, stimuli=obj.id).aggregate(Avg('fa1'))[
            'fa1__avg']
        return stimuli

    def get_fa2_value(self, obj):
        test_result_id = self.context.get('view').kwargs['pk']
        stimuli = TestResultStimuli.objects.filter(test_result=test_result_id, stimuli=obj.id).aggregate(Avg('fa2'))[
            'fa2__avg']
        return stimuli

    def get_tar_value(self, obj):
        test_result_id = self.context.get('view').kwargs['pk']
        stimuli = TestResultStimuli.objects.filter(test_result=test_result_id, stimuli=obj.id).aggregate(Avg('tar'))[
            'tar__avg']
        return stimuli

    def get_coh_value(self, obj):
        test_result_id = self.context.get('view').kwargs['pk']
        wave1 = TestResultStimuli.objects.values_list('wave1', flat=True).filter(test_result=test_result_id,
                                                                                 stimuli=obj.id)
        wave2 = TestResultStimuli.objects.values_list('wave2', flat=True).filter(test_result=test_result_id,
                                                                                 stimuli=obj.id)
        wave3 = TestResultStimuli.objects.values_list('wave3', flat=True).filter(test_result=test_result_id,
                                                                                 stimuli=obj.id)
        pc1 = np.nanmean(signal.coherence(wave1, wave2)[1]) if np.any(
            np.isfinite(signal.coherence(wave1, wave2)[1])) else 1
        pc2 = np.nanmean(signal.coherence(wave1, wave3)[1]) if np.any(
            np.isfinite(signal.coherence(wave1, wave3)[1])) else 1
        pc3 = np.nanmean(signal.coherence(wave2, wave3)[1]) if np.any(
            np.isfinite(signal.coherence(wave2, wave3)[1])) else 1
        pc = (pc1 + pc2 + pc3) / 3 * 100
        return pc
