from django.urls import path
from .views import Home, AgentList, AgentDetails, AgentListingsList, AgentListingsDetails, ListingList, ClientList, ClientDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('agents/', AgentList.as_view(), name='property-list'),
    path('agentdetails/<int:id>/', AgentDetails.as_view(), name='agent-details'),
    path('agentlisting/', AgentListingsList.as_view(), name='agent-list'),
    path('agentlistingdetails/<int:id>/', AgentListingsDetails.as_view(), name='agent-listing-details'),
    path('listinglist/', ListingList.as_view(), name='listing-list'),
    path('clientlist/', ClientList.as_view(), name='client-list'),
    path('clientdetail/', ClientDetail.as_view(), name='client-detail'),
    
]
