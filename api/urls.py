from django.urls import path
from .views import(get_user, get_listings, create_listing, 
	NewUserView, logout_view, delete_listing, my_listings, CookieTokenRefreshView, CookieTokenObtainPairView
) 
urlpatterns = [
	path('user', get_user, name='get_user_root'), 
	path('get_listings', get_listings, name='get_listings_root'),
	path('create-listing/', create_listing, name='create-listing'),
	path('listings/my', my_listings, name='my-listings'),
	path('listings/<int:pk>/', delete_listing),
	path('signup/', NewUserView.as_view(), name='signup'),
	path('logout/', logout_view, name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('token/obtain/', CookieTokenObtainPairView.as_view(), name='token_obtain'),

]