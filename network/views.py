from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Node, Edge, RouteHistory
from .serializers import NodeSerializer, EdgeSerializer, ShortestRouteSerializer
from .utils import dijkstra


# ✅ Add Node
class NodeCreateView(generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


# ✅ List Nodes
class NodeListView(generics.ListAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


# ✅ Add Edge
class EdgeCreateView(generics.CreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


# ✅ List Edges
class EdgeListView(generics.ListAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


# 🚀 Shortest Route
class ShortestRouteView(APIView):

    def post(self, request):
        serializer = ShortestRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_id = serializer.validated_data['source_id']
        destination_id = serializer.validated_data['destination_id']

        try:
            source = Node.objects.get(id=source_id)
            destination = Node.objects.get(id=destination_id)
        except Node.DoesNotExist:
            return Response({"error": "Invalid nodes"}, status=400)

        total_latency, path_ids = dijkstra(source_id, destination_id)

        if total_latency is None:
            return Response(
                {"error": "No path exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Convert IDs → names
        path_names = list(Node.objects.filter(id__in=path_ids).values_list('name', flat=True))

        # Save history
        RouteHistory.objects.create(
            source=source,
            destination=destination,
            total_latency=total_latency,
            path=path_names
        )

        return Response({
            "total_latency": total_latency,
            "path": path_names
        })


# 📜 Route History
class RouteHistoryView(generics.ListAPIView):
    serializer_class = NodeSerializer  # override below

    def get_queryset(self):
        queryset = RouteHistory.objects.all().order_by('-created_at')

        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')
        limit = self.request.query_params.get('limit')

        if source:
            queryset = queryset.filter(source__id=source)

        if destination:
            queryset = queryset.filter(destination__id=destination)

        if limit:
            queryset = queryset[:int(limit)]

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = [
            {
                "id": r.id,
                "source": r.source.name,
                "destination": r.destination.name,
                "total_latency": r.total_latency,
                "path": r.path,
                "created_at": r.created_at
            }
            for r in queryset
        ]

        return Response(data)