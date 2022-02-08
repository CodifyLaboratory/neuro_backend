from django.urls import path

from .views import TestViewSet, StimuliCategoryViewSet, StimuliViewSet, TestResultViewSet, \
    CalculationViewSet, ParameterViewSet, OperationViewSet, TestResultFileViewSet

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
    path('calculations/', CalculationViewSet.as_view({'get': 'list'})),
    path('calculations/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve'})),
    path('calculations/update/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('calculations/delete/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Test Results
    path('results/create/', TestResultViewSet.as_view({'post': 'create'})),
    path('results/', TestResultViewSet.as_view({'get': 'list'})),
    path('results/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve'})),
    path('results/update/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('results/delete/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    path('results/export/<int:pk>/', TestResultFileViewSet.as_view({'get': 'retrieve'})),
]