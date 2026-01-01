from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.models import NewUser 
from listings.models import Listing 
from users.serializers import NewUserSerializer
from listings.serializers import ListingSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


#class GoogleLogin(SocialLoginView):
 #   adapter_class = GoogleOAuth2Adapter
  #  client_class = OAuth2Client


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get("refresh")
        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=False,  # True in production
                samesite="Lax",
            )
        return response



class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")

        if not refresh:
            return Response(
                {"detail": "No refresh token cookie"},
                status=status.HTTP_401_UNAUTHORIZED,
                )
        serializer = self.get_serializer(data={"refresh":refresh})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_listing(request):
    serializer = ListingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    #Ensure only the owner can delete
    if listing.user != request.user:
        return Response(
            {"detail": "You do not have permission to delete this listing,"},
                status=status.HTTP_400_FORBIDDEN
            )
    listing.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = NewUserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
def get_listings(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)


class NewUserView(generics.CreateAPIView):
    serializer_class = NewUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message":"User registered successfully."})
#@api_view(['GET'])
#def get_seller(request):
 #   seller = SellerProfile.objects.all()
  #  serializer = SellerProfileSerializer(seller, many=True)
   # return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # If using Token authentication
    request.user.auth_token.delete()
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_listings(request):
    listings = Listing.objects.filter(user=request.user)
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)
