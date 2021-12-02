from decouple import config
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .cortex import Cortex
from .models import Test, StimuliCategory, Stimulus, TestResult
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, HeadsetSerializer, GetUserSerializer, CreateSessionSerializer, CloseSessionSerializer


class StimuliCategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = StimuliCategory.objects.all()
    serializer_class = StimuliCategorySerializer


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
            # elif self.action == 'retrieve' or self.action == 'list':
            #     return TestResultDetailSerializer
        except:
            raise PermissionDenied

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cortex_token = request.data['cortex_token']
        headset = request.data['headset']
        record_name = request.data['title']
        try:
            c = Cortex(user=user)
            session = c.create_session(cortex_token=cortex_token, headset=headset)
            if 'result' in session:
                stream = c.subscribe_request(cortex_token=cortex_token, session_id=session['result']['id'])
                if 'result' in stream:
                    record = c.create_record(cortex_token=cortex_token, session_id=session['result']['id'],
                                             record_name=record_name)
                    if 'result' in record:
                        c.stop_record(cortex_token=cortex_token, session_id=session['result']['id'])
                        c.disconnect_headset(headset_id=headset)
                        print(record['result']['uuid'])
                        export = c.export_record(cortex_token=cortex_token, record_ids=record['result']['uuid'],
                                                 folder='/media/results/')
                        print(export)
                        if 'result' in export:
                            serializer.save()
                            return serializer
                        else:
                            return Response({
                                'error': export['error']['message'],
                            }, 400)
                    else:
                        return Response({
                            'error': record['error']['message'],
                        }, 400)
                else:
                    return Response({
                        'error': stream['error']['message'],
                    }, 400)
            else:
                return Response({
                    'error': session['error']['message'],
                }, 400)
        except:
            return Response(serializer.errors, 400)

user = {
    "license": "",
    "client_id": config('CLIENT_ID'),
    "client_secret": config('CLIENT_SECRET'),
    "debit": 100
}


@api_view()
def create_session(request):
    serializer = CreateSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@api_view()
def request_access(request):
    c = Cortex(user=user)
    result = c.request_access()
    return Response({
        'result': result,
    })


@api_view()
def authorize(request):
    c = Cortex(user=user)
    result = c.authorize()
    return Response({
        'result': result,
    })


@api_view()
def get_user_info(request):
    serializer = GetUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    c = Cortex(user=user)
    result = c.get_user_info(cortex_token=serializer.data['cortex_token'])
    return Response({
        'result': result,
    })


@api_view()
def info(request):
    c = Cortex(user=user)
    result = c.get_cortex_info()
    return Response({
        'id': result['id'],
        'jsonrpc': result['jsonrpc']
    })


@api_view()
def get_headset(request):
    c = Cortex(user=user)
    result = c.query_headset()
    return Response({
        'result': result,
    })


@api_view()
def connect_headset(request):
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    c = Cortex(user=user)
    result = c.connect_headset(headset_id=serializer.data['headset'])
    return Response({
        'result': result,
    })


@api_view()
def disconnect_headset(request):
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    c = Cortex(user=user)
    result = c.disconnect_headset(headset_id=serializer.data['headset'])
    return Response({
        'result': result,
    })


@api_view()
def close_session(request):
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    c = Cortex(user=user)
    result = c.close_session(cortex_token=serializer.data['cortex_token'], session_id=serializer.data['session_id'])

    return Response({
        'result': result,
    })


# @api_view()
# def subscribe_request(request):
#     serializer = SubscribeDataSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     c = Cortex(user=user)
#     result = c.subscribe_request(cortex_token=serializer.data['cortex_token'], session_id=serializer.data['session_id'])
#     return Response({
#         'result': result,
#     })

@api_view()
def get_session(request):
    serializer = GetUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    c = Cortex(user=user)
    result = c.get_session(cortex_token=serializer.data['cortex_token'])
    return Response({
        'result': result,
    })
