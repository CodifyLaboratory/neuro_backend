from django.urls import path

from .views import TestViewSet, StimuliCategoryViewSet, StimuliViewSet, TestResultViewSet, get_headset, \
    connect_headset, disconnect_headset, authorize, create_session, close_session, \
    export_record, CortexClientViewSet, TestSessionViewSet, \
    get_query_session, stop_test, generate_ngrok_url, create_connection, CalculationViewSet, ParameterViewSet, \
    OperationViewSet

urlpatterns = [
    # Categories and Parameters
    path('categories/', StimuliCategoryViewSet.as_view({'get': 'list'})),
    path('parameters/', ParameterViewSet.as_view({'get': 'list'})),
    path('operations/', OperationViewSet.as_view({'get': 'list'})),

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

    # Calculation
    path('calculations/create/<int:pk>/', CalculationViewSet.as_view({'post': 'create'})),
    path('calculations/', CalculationViewSet.as_view({'get': 'list'})),
    path('calculations/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve'})),
    path('calculations/update/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('calculations/delete/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Test Results
    path('results/create/<int:pk>/', TestResultViewSet.as_view({'post': 'create'})),
    path('sessions/create/<int:pk>/', TestSessionViewSet.as_view({'post': 'create'})),
    path('results/', TestResultViewSet.as_view({'get': 'list'})),
    path('results/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve'})),
    path('results/update/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('results/delete/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Get headset
    path('headsets/', get_headset),
    path('get-headset/', get_headset),
    path('connect-headset/', connect_headset),
    path('disconnect-headset/', disconnect_headset),

    path('get-cortex-token/', authorize),

    path('create-session/', create_session),
    path('close-session/', close_session),
    path('query-sessions/', get_query_session),

    path('stop-session/', stop_test),

    # path('subscribe_data/', subscribe_request),

    path('export-record/', export_record),
    # path('start-session/', _start_session),
    # path('close-session/', _stop_session),

    #Cortex Client URL
    path('cortex-url/create/', CortexClientViewSet.as_view({'post': 'create'})),
    path('cortex-url/update/<int:pk>/', CortexClientViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('cortex-url/get/', CortexClientViewSet.as_view({'get': 'list'})),


    path('generate-ngrok-url/', generate_ngrok_url),
    path('ws/', create_connection),

]