from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import TravelRequest
from .serializers import TravelRequestSerializer, TravelRequestCreateSerializer


class TravelRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Travel Requests'],
        summary='List All Travel Requests',
        description='Returns a paginated list of all customer travel requests.',
        parameters=[
            OpenApiParameter('search', OpenApiTypes.STR, description='Search by name, destination or purpose'),
            OpenApiParameter('page',   OpenApiTypes.INT, description='Page number',      default=1),
            OpenApiParameter('limit',  OpenApiTypes.INT, description='Results per page', default=10),
        ],
        responses={200: TravelRequestSerializer(many=True)},
    )
    def get(self, request):
        search = request.query_params.get('search', '')
        page   = int(request.query_params.get('page',  1))
        limit  = int(request.query_params.get('limit', 10))

        requests = TravelRequest.objects.all()

        if search:
            requests = requests.filter(
                Q(full_name__icontains=search)       |
                Q(destination__icontains=search)     |
                Q(travel_purpose__icontains=search)  |
                Q(email__icontains=search)
            )

        total     = requests.count()
        start     = (page - 1) * limit
        end       = start + limit
        paginated = requests[start:end]
        serializer = TravelRequestSerializer(paginated, many=True)

        return Response({
            'status' : 'success',
            'total'  : total,
            'page'   : page,
            'limit'  : limit,
            'pages'  : (total + limit - 1) // limit,
            'data'   : serializer.data
        }, status=status.HTTP_200_OK)


class TravelRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Travel Requests'],
        summary='Get Single Travel Request',
        description='Returns full details of a specific travel request by ID.',
        responses={200: TravelRequestSerializer},
    )
    def get(self, request, pk):
        try:
            travel_request = TravelRequest.objects.get(pk=pk)
            serializer     = TravelRequestSerializer(travel_request)
            return Response({
                'status' : 'success',
                'data'   : serializer.data
            }, status=status.HTTP_200_OK)
        except TravelRequest.DoesNotExist:
            return Response({
                'status'  : 'error',
                'message' : 'Travel request not found'
            }, status=status.HTTP_404_NOT_FOUND)


class TravelRequestCreateView(APIView):
    """
    Public endpoint — used by the customer-facing website.
    No authentication required.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Travel Requests'],
        summary='Submit Travel Request (Public)',
        description='Allows website visitors to submit a travel request. No authentication required.',
        request=TravelRequestCreateSerializer,
        responses={201: TravelRequestSerializer},
    )
    def post(self, request):
        serializer = TravelRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            travel_request = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Your travel request has been submitted successfully. We will get back to you shortly.',
                'data'    : TravelRequestSerializer(travel_request).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)