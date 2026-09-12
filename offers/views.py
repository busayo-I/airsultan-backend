from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Offer
from .serializers import OfferSerializer, OfferCreateUpdateSerializer


class OfferListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    @extend_schema(
        tags=['Offers'],
        summary='List All Offers',
        description='Returns a paginated list of all offers. Supports search by title, type, or provider.',
        parameters=[
            OpenApiParameter('search', OpenApiTypes.STR,  description='Search by title, type or provider'),
            OpenApiParameter('page',   OpenApiTypes.INT,  description='Page number', default=1),
            OpenApiParameter('limit',  OpenApiTypes.INT,  description='Results per page', default=10),
        ],
        responses={200: OfferSerializer(many=True)},
    )
    def get(self, request):
        search = request.query_params.get('search', '')
        page   = int(request.query_params.get('page',  1))
        limit  = int(request.query_params.get('limit', 10))

        offers = Offer.objects.all()

        if search:
            offers = offers.filter(
                Q(title__icontains=search)    |
                Q(type__icontains=search)     |
                Q(provider__icontains=search)
            )

        total        = offers.count()
        start        = (page - 1) * limit
        end          = start + limit
        paginated    = offers[start:end]
        serializer   = OfferSerializer(paginated, many=True, context={'request': request})

        return Response({
            'status'  : 'success',
            'total'   : total,
            'page'    : page,
            'limit'   : limit,
            'pages'   : (total + limit - 1) // limit,
            'data'    : serializer.data,
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Offers'],
        summary='Create New Offer',
        description='Create a new travel offer with banner image upload.',
        request=OfferCreateUpdateSerializer,
        responses={201: OfferSerializer},
    )
    def post(self, request):
        serializer = OfferCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            offer = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Offer created successfully',
                'data'    : OfferSerializer(offer, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return None

    @extend_schema(
        tags=['Offers'],
        summary='Get Single Offer',
        description='Returns details of a specific offer by ID.',
        responses={200: OfferSerializer},
    )
    def get(self, request, pk):
        offer = self.get_object(pk)
        if not offer:
            return Response({
                'status'  : 'error',
                'message' : 'Offer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSerializer(offer, context={'request': request})
        return Response({
            'status' : 'success',
            'data'   : serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Offers'],
        summary='Update Offer',
        description='Update an existing offer by ID.',
        request=OfferCreateUpdateSerializer,
        responses={200: OfferSerializer},
    )
    def put(self, request, pk):
        offer = self.get_object(pk)
        if not offer:
            return Response({
                'status'  : 'error',
                'message' : 'Offer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferCreateUpdateSerializer(
            offer, data=request.data, partial=True
        )
        if serializer.is_valid():
            offer = serializer.save()
            return Response({
                'status'  : 'success',
                'message' : 'Offer updated successfully',
                'data'    : OfferSerializer(offer, context={'request': request}).data
            }, status=status.HTTP_200_OK)

        return Response({
            'status'  : 'error',
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Offers'],
        summary='Delete Offer',
        description='Delete an offer by ID.',
        responses={200: None},
    )
    def delete(self, request, pk):
        offer = self.get_object(pk)
        if not offer:
            return Response({
                'status'  : 'error',
                'message' : 'Offer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        offer.delete()
        return Response({
            'status'  : 'success',
            'message' : 'Offer deleted successfully'
        }, status=status.HTTP_200_OK)
