from django.urls import path

from .views import TestViewSet, StimuliCategoryViewSet, StimuliViewSet, TestResultViewSet, \
    TestCalculationViewSet, ParameterViewSet, TestResultExportViewSet

urlpatterns = [
    # Categories and Parameters
    path('categories/', StimuliCategoryViewSet.as_view({'get': 'list'})),
    path('parameters/', ParameterViewSet.as_view({'get': 'list'})),

    # Tests
    path('tests/create/', TestViewSet.as_view({'post': 'create'})),
    path('tests/', TestViewSet.as_view({'get': 'list'})),
    path('tests/<int:pk>/', TestViewSet.as_view({'get': 'retrieve'})),
    path('tests/update/<int:pk>/', TestViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('tests/delete/<int:pk>/', TestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Calculation
    path('calculations/<int:pk>/', TestCalculationViewSet.as_view({'get': 'retrieve', 'put': 'update'})),

    # Stimuli
    path('stimulus/create/<int:pk>/', StimuliViewSet.as_view({'post': 'create'})),
    path('test/stimuluses/<int:pk>/', StimuliViewSet.as_view({'get': 'list'})),
    path('stimulus/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve'})),
    path('stimulus/update/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('stimulus/delete/<int:pk>/', StimuliViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    # Test Results
    path('results/create/', TestResultViewSet.as_view({'post': 'create'})),
    path('results/', TestResultViewSet.as_view({'get': 'list'})),
    path('results/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve'})),
    path('results/update/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('results/delete/<int:pk>/', TestResultViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),

    path('results/export/<int:pk>/', TestResultExportViewSet.as_view({'get': 'retrieve'})),
    # path('results-view/export/<int:pk>/', TestResultExportViewSet.as_view({'get': 'retrieve'})),
]