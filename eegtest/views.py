import json
import ssl
import time

import websocket
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .cortex import Cortex
from .models import Test, StimuliCategory, Stimulus, TestResult, CortexSessionModel
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, HeadsetSerializer, GetUserSerializer, CreateSessionSerializer, CloseSessionSerializer, \
    ExportRecordSerializer, CortexClientSerializer, CreateSession1Serializer

from user.models import User

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


# def get_current_user(request):
#     url = CortexSessionModel.objects.get(user=request.user).url
#     return str(url)

c = Cortex(user={"license": "",
                 "client_id": config('CLIENT_ID'),
                 "client_secret": config('CLIENT_SECRET'),
                 "debit": 100}
           )


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
            raise NotAuthenticated

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headset = request.data['headset']
        # try:
        #     c.url = CortexSessionModel.objects.get(user=self.request.user).url
        # except:
        #     return Response(401)
        token = c.authorize()
        cortex_token = token['result']['cortexToken']
        session = c.create_session(cortex_token=cortex_token, headset=headset)
        if 'error' in session:
            return Response({
                'error': session['error']}, 400)
        session_id = session['result']['id']
        stream = c.subscribe_request(cortex_token=token, session_id=session_id)
        record_name = User.objects.get(id=self.request.user.id).email
        record = c.create_record(cortex_token=cortex_token, session_id=session_id,
                                 record_name=record_name)
        record_id = record['result']['record']['uuid']
        serializer.save()
        return Response({
            'session_id': session_id,
            'record_id': record_id,
        }, 201)


@api_view()
def stop_test(request):
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token = c.authorize()
    cortex_token = token['result']['cortexToken']
    record = c.stop_record(cortex_token=cortex_token, session_id=serializer.data['session_id'])
    session = c.close_session(cortex_token=cortex_token, session_id=serializer.data['session_id'])
    return Response({
        'result': record,
    })


# time.sleep(6)
# print(record)
# if 'result' in record:
#     c.stop_record(cortex_token=cortex_token, session_id=session['result']['id'])
#     c.unsubscribe_request(cortex_token=cortex_token, session_id=session['result']['id'])
#     c.close_session(cortex_token=cortex_token, session_id=session['result']['id'])
#     c.disconnect_headset(headset_id=headset)
#     time.sleep(1)
#     export = c.export_record(cortex_token=cortex_token,
#                              record_ids=[record['result']['record']['uuid']],
#                              folder='/media')
#     print(export)
#     if 'pow' in export:
#         serializer.save()
#         return Response(serializer, 201)
#     else:
#         return Response({
#             'error': export['result']['message'],
#         }, 400)


@api_view()
def request_access(request):
    result = c.request_access()
    return Response({
        'result': result,
    })


@api_view()
def authorize(request):

    result = c.authorize()
    return Response({
        'result': result,
    })


@api_view()
def get_user_info(request):
    serializer = GetUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.get_user_info(cortex_token=serializer.data['cortex_token'])
    return Response({
        'result': result,
    })


@api_view()
def info(request):
    url = CortexSessionModel.objects.get(user=request.user).url
    c.ws_connect(url)
    result = c.get_cortex_info()
    print(c.ws.connected)
    print(url)
    return Response({
        'id': result['id'],
        'jsonrpc': result['jsonrpc']
    })





# @api_view()
# def get_headset(request):
#     try:
#         c.url = CortexSessionModel.objects.get(user=request.user).url
#         print(c.url)
#     except:
#         raise NotAuthenticated
#     result = c.query_headset()
#     if result['result'] == []:
#         return Response({
#             'result': result}, 404)
#     return Response({
#         'result': result}, 200)

@api_view()
def get_headset(request):
    result = c.query_headset()
    if result['result'] == []:
        return Response({
            'result': result}, 404)
    return Response({
        'result': result['result']}, 200)


# @api_view()
# def get_headset(request):
#     ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
#         ws.connect(url=self.url)
#     result = c.query_headset()
#     if result['result'] == []:
#         return Response({
#             'result': result}, 404)
#     return Response({
#         'result': result['result']}, 200)

@api_view()
def connect_headset(request):
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.connect_headset(headset_id=serializer.data['headset'])
    return Response({
        'result': result}, 200)


@api_view()
def disconnect_headset(request):
    serializer = HeadsetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.disconnect_headset(headset_id=serializer.data['headset'])
    return Response({
        'result': result,
    })


@api_view()
def create_record(request):
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    test_result = TestResult.objects.create(user=request.user, )
    result = c.close_session(cortex_token=serializer.data['cortex_token'], session_id=serializer.data['session_id'])
    return Response({
        'result': result,
    })


@api_view()
def create_session(request):
    c.ws_connect(url="wss://localhost:6868")
    serializer = CreateSession1Serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.create_session(cortex_token=serializer.data['cortex_token'], headset=serializer.data['headset'])
    return Response({
        'result': result,
    })

@api_view()
def close_session(request):
    c.ws_connect(url="wss://localhost:6868")
    serializer = CloseSessionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.close_session(cortex_token=serializer.data['cortex_token'], session_id=serializer.data['session_id'])
    return Response({
        'result': result,
    })

# @api_view()
# def close_session(request):
#     url = "wss://localhost:6868"
#     ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
#     ws.connect(url=url)
#     serializer = CloseSessionSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     close_session_request = {
#         "jsonrpc": "2.0",
#         "id": 2,
#         "method": "updateSession",
#         "params": {
#             "cortexToken": serializer.data['cortex_token'],
#             "session": serializer.data['session_id'],
#             "status": "close"
#         }
#     }
#     ws.send(json.dumps(close_session_request))
#     time.sleep(1)
#     result = ws.recv()
#     result_dic = json.loads(result)
#     return Response({
#         'result': result_dic,
#     })


# @api_view()
# def close_session(request):
#     serializer = CloseSessionSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     result = c.close_session(cortex_token=serializer.data['cortex_token'], session_id=serializer.data['session_id'])
#     return Response({
#         'result': result,
#     })


@api_view()
def get_query_session(request):
    url = "wss://localhost:6868"
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
    ws.connect(url=url)
    serializer = GetUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    query_session_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "querySessions",
        "params": {
            "cortexToken": serializer.data['cortex_token'],
        }
    }
    ws.send(json.dumps(query_session_request))
    result = ws.recv()
    result_dic = json.loads(result)
    return Response({
        'result': result_dic,
    })


@api_view()
def _start_session(request):
    data = request.data
    cortex_token = data['cortex_token']
    headset = data['headset']
    record_name = data['title']
    session = c.create_session(cortex_token=cortex_token, headset=headset)
    print(session)
    stream = c.subscribe_request(cortex_token=cortex_token, session_id=session['result']['id'])
    record = c.create_record(cortex_token=cortex_token, session_id=session['result']['id'], record_name=record_name)

    return Response({
        'session_id': session['result']['id'],
        'record_id': record['result']['record']['uuid'],
    })


@api_view()
def _stop_session(request):
    try:
        data = request.data
        cortex_token = data['cortex_token']
        session_id = data['session_id']
        record_id = data['record_id']
        stream = c.subscribe_request(cortex_token=cortex_token, session_id=session_id)
        c.stop_record(cortex_token=cortex_token, session_id=session_id)
        res = 'Ok'
    except Exception as ex:
        res = repr(ex)

    return Response({
        'Message': res
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

# @api_view()
# def get_session(request):
#     serializer = GetUserSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     result = c.get_session(cortex_token=serializer.data['cortex_token'])
#     return Response({
#         'result': result,
#     })


@api_view()
def export_record(request):
    serializer = ExportRecordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    result = c.export_record(cortex_token=serializer.data['cortex_token'], record_ids=[serializer.data['record_ids']],
                             folder=serializer.data['folder'])
    return Response({
        'result': result,
    })
