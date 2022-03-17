from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, \
    Calculation, TestResultStimuli
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, ParameterListSerializer, \
    CalculationSerializer, CalculationListSerializer, \
    TestResultListSerializer, TestResultDetailExportSerializer, TestCalculationSerializer, \
    TestResultDetailAdminSerializer


class StimuliCategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = StimuliCategory.objects.all()
    serializer_class = StimuliCategorySerializer


class ParameterViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer


class TestViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return Test.objects.all()
            elif self.action == 'list' and self.request.user.is_professor:
                return Test.objects.all().order_by('id')
            elif self.action == 'list' and self.request.user.is_simple_user:
                return Test.objects.filter(status=True)
        except:
            raise PermissionDenied

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
            raise PermissionDenied


class StimuliViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        test = Test.objects.get(id=self.kwargs['pk'])
        return serializer.save(test=test)

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return Stimulus.objects.all()
            elif self.action == 'list':
                return Stimulus.objects.filter(test=self.kwargs['pk'])
        except:
            raise PermissionDenied

    def get_serializer_class(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
                return StimuliSerializer
            elif self.action == 'retrieve' or self.action == 'list':
                return StimuliListSerializer
        except:
            raise PermissionDenied


class TestCalculationViewSet(ModelViewSet):
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


class TestResultFileViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = TestResult.objects.all()
    serializer_class = TestResultDetailExportSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'


class TestResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy' or self.action == 'retrieve':
                return TestResult.objects.all()
            elif self.action == 'list' and self.request.user.is_professor:
                return TestResult.objects.all()
            elif self.action == 'list' and self.request.user.is_simple_user:
                return TestResult.objects.filter(user=self.request.user, status=True)
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

    # def retrieve(self, request, *args, **kwargs):
    #     # queryset = TestResultStimuli.objects.filter(test_result=self.get_object())
    #     return