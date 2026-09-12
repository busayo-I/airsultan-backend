from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema

from offers.models import Offer
from insights.models import Article
from travel_requests.models import TravelRequest


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Dashboard'],
        summary='Get Dashboard Statistics',
        description='Returns counts for active offers, published posts, and new travel requests.',
        responses={200: None},
    )
    def get(self, request):
        last_7_days = timezone.now() - timedelta(days=7)

        active_offers    = Offer.objects.filter(status='Active').count()
        published_posts  = Article.objects.filter(status='Active').count()
        new_requests     = TravelRequest.objects.filter(
                               created_at__gte=last_7_days
                           ).count()

        return Response({
            'status' : 'success',
            'data'   : {
                'active_offers'   : active_offers,
                'published_posts' : published_posts,
                'new_requests'    : new_requests,
            }
        }, status=status.HTTP_200_OK)