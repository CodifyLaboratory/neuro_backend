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
    TestResultDetailAdminSerializer, TestResultDetailExportSerializer


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
    """ Test Result Export 2 View """
    queryset = TestResultStimuli.objects.all()
    serializer_class = TestResultDetailExportSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'

    sheet_view_options = {
        'showGridLines': True
    }

    column_header = {
        'titles': [
            "Stimuli",
            "AF3/theta, AF3/alpha, AF3/betaL, AF3/betaH, AF3/gamma, "
            "F7/theta, F7/alpha, F7/betaL, F7/betaH, F7/gamma, "
            "F3/theta, F3/alpha, F3/betaL, F3/betaH, F3/gamma, "
            "FC5/theta, FC5/alpha, FC5/betaL, FC5/betaH, FC5/gamma, "
            "T7/theta, T7/alpha, T7/betaL, T7/betaH, T7/gamma, "
            "P7/theta, P7/alpha, P7/betaL, P7/betaH, P7/gamma, "
            "O1/theta, O1/alpha, O1/betaL, O1/betaH, O1/gamma, "
            "O2/theta, O2/alpha, O2/betaL, O2/betaH, O2/gamma, "
            "P8/theta, P8/alpha, P8/betaL, P8/betaH, P8/gamma, "
            "T8/theta, T8/alpha, T8/betaL, T8/betaH, T8/gamma, "
            "FC6/theta, FC6/alpha, FC6/betaL, FC6/betaH, FC6/gamma, "
            "F4/theta, F4/alpha, F4/betaL, F4/betaH, F4/gamma, "
            "F8/theta, F8/alpha, F8/betaL, F8/betaH, F8/gamma, "
            "AF4/theta, AF4/alpha, AF4/betaL, AF4/betaH, AF4/gamma"
        ],
        'column_width': [20, 400],
        'height': 40,
        'style': {
            'alignment': {
                'horizontal': 'general',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
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
        # 'height': 40,
    }