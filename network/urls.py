from django.urls import path
from .views import (
    NodeCreateView, NodeListView,
    EdgeCreateView, EdgeListView,
    ShortestRouteView, RouteHistoryView
)

urlpatterns = [
    path('nodes', NodeCreateView.as_view()),
    path('nodes/list', NodeListView.as_view()),

    path('edges', EdgeCreateView.as_view()),
    path('edges/list', EdgeListView.as_view()),

    path('routes/shortest', ShortestRouteView.as_view()),
    path('routes/history', RouteHistoryView.as_view()),
]