from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer

from .models import Test, StimuliCategory, Stimulus, TestResult, Parameter, \
    Calculation, Operation
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, ParameterListSerializer, \
    CalculationSerializer, CalculationListSerializer, OperationListSerializer, CalculationDetailSerializer, \
    TestResultListSerializer, TestResultFileSerializer


class StimuliCategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = StimuliCategory.objects.all()
    serializer_class = StimuliCategorySerializer


class ParameterViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer


class OperationViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Operation.objects.all()
    serializer_class = OperationListSerializer


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
        except:
            raise PermissionDenied


class StimuliViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Stimulus.objects.all()

    def perform_create(self, serializer):
        test = Test.objects.get(id=self.kwargs['pk'], status=True)
        return serializer.save(test=test)

    def get_serializer_class(self):
        try:
            if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
                return StimuliSerializer
            elif self.action == 'retrieve' or self.action == 'list':
                return StimuliListSerializer
        except:
            raise PermissionDenied


class CalculationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Calculation.objects.all()

    def get_object(self, queryset=None):
        obj = get_object_or_404(Calculation, test=self.kwargs['pk'])
        return obj

    def get_serializer_class(self):
        try:
            if self.action == 'update' or self.action == 'delete':
                return CalculationSerializer
            elif self.action == 'retrieve':
                return CalculationDetailSerializer
            elif self.action == 'list':
                return CalculationListSerializer
        except:
            raise NotAuthenticated


class TestResultFileViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = TestResult.objects.all()
    serializer_class = TestResultDetailSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'


class TestResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # test = Test.objects.get(id=self.kwargs['pk'])
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
                return TestResultDetailSerializer
            elif self.action == 'list':
                return TestResultListSerializer
        except:
            raise PermissionDenied