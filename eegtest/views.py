import json
from rest_framework import views
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Test, StimuliCategory, Stimuli, TestResult
from .serializers import TestListSerializer, TestSerializer, StimuliCategorySerializer, StimuliSerializer, \
    StimuliListSerializer, TestDetailSerializer, TestDetailUpdateSerializer, TestResultSerializer, \
    TestResultDetailSerializer, HeadsetSerializer

from .cortex import Cortex



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
    queryset = Stimuli.objects.all()


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


# class HeadsetView(views.APIView):
#
#     def post(self, request):
#         yourdata= [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
#         results = YourSerializer(yourdata).data
#         return Response(results)
# @api_view()
# def get_headset(request):
#     from .example_epoc_plus import EEG
#     print(EEG().get_headset())
#     if EEG().get_headset() == 1:
#         return Response('Headset yes.', status=200)
#     else:
#         return Response('Headset no.', status=404)

@api_view()
def start(request):
    from .sub_data import start
    try:
        start()
        return 200
    except:
        return 400

user = {
    "license": "26f60052-0070-4b35-9ed8-fec4363edfc6",
    "client_id": "N0mvmXCzhTLbYNVYDkAMmrUf5WK1YlvPA7D0ujZm",
    "client_secret": "3KVc00v5obtcBzo96moG0wjdEjJ8bNjsgeLl3VzGPbTMnp0woJPmB3dBbxOZ00V66XJTKHcWAeldMSbcvmVTQGGHLcPOSJZPWHweWnVvGUTu1b6a8NxlyWqLWrHf8WgA",
    "debit": 100
}

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
    print(serializer.data['headset'])
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
    print(serializer.data['headset'])
    result = c.disconnect_headset(headset_id=serializer.data['headset'])
    return Response({
        'result': result,
    })



