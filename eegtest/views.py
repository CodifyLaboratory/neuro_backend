from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from user.models import User
from .connection import ws_connections
from .models import Test, StimuliCategory, Stimulus, TestResult, CortexSessionModel, CortexObjectModel, Parameter, \
    Calculation, Operation
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, HeadsetSerializer, GetUserSerializer, CreateSessionSerializer, CloseSessionSerializer, \
    ExportRecordSerializer, CortexClientSerializer, CreateSession1Serializer, ParameterListSerializer, \
    CalculationSerializer, CalculationListSerializer, OperationListSerializer, CalculationDetailSerializer


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


class TestResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        test = Test.objects.get(id=self.kwargs['pk'])
        return serializer.save(user=self.request.user, test=test)

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
            elif self.action == 'retrieve' or self.action == 'list':
                return TestResultDetailSerializer
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


class CortexClientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CortexClientSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        try:
            if self.action == 'create':
                return CortexSessionModel.objects.all()
            elif self.action == 'update' or self.action == 'retrieve' or self.action == 'list':
                return CortexSessionModel.objects.filter(user=self.request.user)
        except:
            raise PermissionDenied


class TestSessionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        test = Test.objects.get(id=self.kwargs['pk'])
        return serializer.save(user=self.request.user, test=test)

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
                return CreateSessionSerializer
        except:
            raise NotAuthenticated

    def create(self, request, *args, **kwargs):
        cortex = CortexObjectModel.objects.get(user=request.user)
        if not ws_connections or ws_connections[request.user.id].connected == False:
            cortex._ws_connection()
        ws = ws_connections[request.user.id]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headset = request.data['headset']
        token = cortex.authorize(ws)
        cortex_token = token['result']['cortexToken']
        session = cortex.create_session(ws, cortex_token=cortex_token, headset=headset)
        if 'error' in session:
            return Response({
                'error': session['error']}, 400)
        session_id = session['result']['id']
        stream = cortex.subscribe_request(ws, cortex_token=token, session_id=session_id)
        record_name = User.objects.get(id=self.request.user.id).email
        record = cortex.create_record(ws, cortex_token=cortex_token, session_id=session_id,
                                      record_name=record_name)
        record_id = record['result']['record']['uuid']
        serializer.save()
        return Response({
            'session_id': session_id,
            'record_id': record_id,
        }, 201)


@api_view()
def stop_test(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = cortex.authorize(ws)
    cortex_token = token['result']['cortexToken']
    record = cortex.stop_record(ws, cortex_token=cortex_token, session_id=serializer.data['session_id'])
    session = cortex.close_session(ws, cortex_token=cortex_token, session_id=serializer.data['session_id'])
    return Response({
        'result': record,
    })


# GET CORTEX TOKEN
@api_view()
def authorize(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    print(ws_connections)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    result = cortex.authorize(ws)
    return Response({
        'result': result,
    })

@api_view()
def generate_ngrok_url(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    cortex.generate_tcp_url()
    return Response({
        'result': cortex.url}, 200)

@api_view()
def create_connection(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    cortex._ws_connection()
    return Response({
        'result': cortex.url}, 200)


# GET QUERY HEADSETS
@api_view(['GET', 'POST'])
def get_headset(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    print(ws_connections)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    result = cortex.query_headset(ws)
    if result['result'] == []:
        return Response({
            'result': result}, 404)
    return Response({
        'result': result['result']}, 200)


@api_view(['GET', 'POST'])
def connect_headset(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex.connect_headset(ws, headset_id=serializer.data['headset'])
    return Response({
        'result': result}, 200)


@api_view(['GET', 'POST'])
def disconnect_headset(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex.disconnect_headset(ws, headset_id=serializer.data['headset'])
    return Response({
        'result': result,
    })


@api_view(['GET', 'POST'])
def create_session(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = CreateSession1Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex._create_session(ws, cortex_token=serializer.data['cortex_token'],
                                    headset=serializer.data['headset'])
    return Response({
        'result': result,
    })


@api_view(['GET', 'POST'])
def close_session(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex._close_session(ws, cortex_token=serializer.data['cortex_token'],
                                   session_id=serializer.data['session_id'])
    return Response({
        'result': result,
    })


@api_view()
def get_query_session(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = GetUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex._get_query_session(ws, cortex_token=serializer.data['cortex_token'])
    return Response({
        'result': result,
    })


@api_view()
def export_record(request):
    cortex = CortexObjectModel.objects.get(user=request.user)
    if not ws_connections or ws_connections[request.user.id].connected == False:
        cortex._ws_connection()
    ws = ws_connections[request.user.id]
    serializer = ExportRecordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = cortex.export_record(cortex_token=serializer.data['cortex_token'],
                                  record_ids=[serializer.data['record_ids']],
                                  folder=serializer.data['folder'])
    return Response({
        'result': result,
    })
