from django.urls import path

from .views import TestViewSet, StimuliCategoryViewSet, StimuliViewSet, TestResultViewSet, get_headset, info, \
    connect_headset, disconnect_headset, request_access, authorize, get_user_info, create_session, close_session, \
    get_session

urlpatterns = [
    # Categories
    path('categories/', StimuliCategoryViewSet.as_view({'get': 'list'})),

    # Tests
    path('tests/create/', TestViewSet.as_view({'post': 'create'})),
    path('tests/', TestViewSet.as_view({'get': 'list'})),
    path('tests/<int:pk>/', TestViewSet.as_view({'get': 'retrieve'})),
    path('tests/update/<int:pk>/', TestViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('tests/delete/<int:pk>/', TestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Stimuli
    path('stimulus/create/<int:pk>/', StimuliViewSet.as_view({'post': 'create'})),
    path('stimulus/', StimuliViewSet.as_view({'get': 'list'})),
    path('stimulus/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve'})),
    path('stimulus/update/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('stimulus/delete/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Test Results
    path('results/create/<int:pk>/', TestResultViewSet.as_view({'post': 'create'})),
    path('results/', TestResultViewSet.as_view({'get': 'list'})),
    path('results/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve'})),
    path('results/update/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('results/delete/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Get headset
    path('headsets/', get_headset),
    path('info/', info),
    path('get-headset/', get_headset),
    path('connect-headset/', connect_headset),
    path('disconnect-headset/', disconnect_headset),
    path('request-access/', request_access),
    path('get-cortex-token/', authorize),
    path('get-user-info/', get_user_info),
    path('create-session/', create_session),
    path('close-session/', close_session),
    # path('subscribe_data/', subscribe_request),
    path('query-sessions/', get_session),


]