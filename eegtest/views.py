from rest_framework.exceptions import PermissionDenied, NotAuthenticated, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, TestResultStimuli
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    ParameterListSerializer, TestResultListSerializer, TestCalculationSerializer, \
    TestResultDetailAdminSerializer, TestResultDetailExportSerializer, TestResultDetailAdminExportSerializer


class StimuliCategoryViewSet(ReadOnlyModelViewSet):
    """ Stimuli Category View """
    permission_classes = [IsAuthenticated, ]
    queryset = StimuliCategory.objects.all()
    serializer_class = StimuliCategorySerializer


class ParameterViewSet(ReadOnlyModelViewSet):
    """ Parameter View """
    permission_classes = [IsAuthenticated]
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer


class TestViewSet(ModelViewSet):
    """ Test View """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return Test.objects.all()
            elif self.action == 'list' and self.request.user.is_professor:
                return Test.objects.all().order_by('-id')
            elif self.action == 'list' and self.request.user.is_simple_user:
                return Test.objects.filter(status=True).order_by('-id')
        except:
            raise NotAuthenticated

    def get_serializer_class(self):
        try:
            if self.action == 'create' or self.action == 'destroy':
                return TestSerializer
            elif self.action == 'retrieve':
                return TestDetailSerializer
            elif self.action == 'update':
                return TestDetailUpdateSerializer
            elif self.action == 'list':
                return TestListSerializer
            elif self.action == 'calculation':
                return TestDetailUpdateSerializer
        except:
            raise NotAuthenticated


class StimuliViewSet(ModelViewSet):
    """ Stimuli View """
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        test = Test.objects.get(id=self.kwargs['pk'])
        return serializer.save(test=test)

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return Stimulus.objects.all()
            elif self.action == 'list':
                return Stimulus.objects.filter(test=self.kwargs['pk']).order_by('-id')
        except:
            raise NotAuthenticated

    def get_serializer_class(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
                return StimuliSerializer
            elif self.action == 'retrieve' or self.action == 'list':
                return StimuliListSerializer
        except:
            raise NotAuthenticated


class TestCalculationViewSet(ModelViewSet):
    """ Test Calculation View Set """
    permission_classes = [IsAuthenticated, ]
    queryset = Test.objects.all()

    def get_serializer_class(self):
        try:
            if self.action == 'update':
                return TestCalculationSerializer
            elif self.action == 'retrieve':
                return TestCalculationSerializer
        except:
            raise NotAuthenticated

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class TestResultViewSet(ModelViewSet):
    """ Test Result View Set """
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return TestResult.objects.all()
            elif self.action == 'list' and self.request.user.is_professor:
                return TestResult.objects.all().order_by('-id')
            elif self.action == 'list' and self.request.user.is_simple_user:
                return TestResult.objects.filter(user=self.request.user, status=True).order_by('-id')
        except:
            raise PermissionDenied

    def get_serializer_class(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
                return TestResultSerializer
            elif self.action == 'retrieve':
                return TestResultDetailAdminSerializer
            elif self.action == 'list':
                return TestResultListSerializer
        except:
            raise PermissionDenied


class TestResultExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """ Test Result Export View """
    serializer_class = TestResultDetailExportSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'

    def get_queryset(self):
        return TestResultStimuli.objects.filter(test_result_id=self.kwargs['pk'])

    column_header = {
        'titles': [
            "Stimulus Name",
        ],
        'style': {
            'alignment': {
                'horizontal': 'general',
                'vertical': 'center',
            },
            'font': {
                'name': 'Calibri',
                'size': 12,
                'color': 'FF000000',
            },
        },
    }

    body = {
        'style': {
            'alignment': {
                'horizontal': 'general',
                'vertical': 'center',
            },
            'font': {
                'name': 'Arial',
                'size': 11,
                'color': 'FF000000',
            }
        },
    }


class TestResultParametersExportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    """ Test Result Export 2 View """
    serializer_class = TestResultDetailAdminExportSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'

    def get_queryset(self):
        return Stimulus.objects.filter(test_results_stimulus__test_result_id=self.kwargs['pk']).distinct()

    column_header = {
        'titles': [
            "Stimulus Name",
            "Frontal Asymmetry 1 Value",
            "Frontal Asymmetry 2 Value",
            "Beta Coherence Value",
            "Cognitive Load TAR Value",
        ],
        'style': {
            'alignment': {
                'horizontal': 'general',
                'vertical': 'center',
            },
            'font': {
                'name': 'Calibri',
                'size': 12,
                'color': 'FF000000',
            },
        },
    }

    body = {
        'style': {
            'alignment': {
                'horizontal': 'general',
                'vertical': 'center',
            },
            'font': {
                'name': 'Arial',
                'size': 11,
                'color': 'FF000000',
            }
        },
    }