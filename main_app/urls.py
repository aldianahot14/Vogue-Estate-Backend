from django.urls import path
from .views import Home, AgentList, AgentDetails, AgentListingsList, AgentListingsDetails, ListingList, ClientList, ClientDetail, CreateAgentView, VerifyAgentView, LoginAgentView, CreateClientView, LoginClientView, ListingDetails

urlpatterns = [
    # home
    path('', Home.as_view(), name='home'),
    # brings up list of all agents and their listings
    path('agents/', AgentList.as_view(), name='property-list'),
    # brings up list of all listings for that agent and their info via the agent id, perform Get Put Delete
    path('agentdetails/<int:id>/', AgentDetails.as_view(), name='agent-detail'),
    # brings up list of agents listings
    path('agentlisting/<int:user_id>/', AgentListingsList.as_view(), name='agent-list'),
    # brings up that particular listing and all its details, also use for Get Put Delete 
    path('agentlistingdetails/<int:id>/', AgentListingsDetails.as_view(), name='agent-listing-details'),
    # works
    path('agents/token/refresh/', VerifyAgentView.as_view(), name='token_refresh'),
    # works
    path('agents/register/', CreateAgentView.as_view(), name='register'),
    # works
    path('agents/login/', LoginAgentView.as_view(), name='login'),
    # brings up list of all clients
    path('clientlist/', ClientList.as_view(), name='client-list'),
    # returns particular client details, perform Get Put Delete
    path('clientdetail/<int:id>/', ClientDetail.as_view(), name='client-detail'),
    # works Create client
    path('client/register/', CreateClientView.as_view(), name='register'),
    # works
    path('client/login/', LoginClientView.as_view(), name='register'), 
    # brings up list of all listings
    path('listinglist/', ListingList.as_view(), name='listing-list'),
    # U G D by id
    path('listing/<int:id>/', ListingDetails.as_view(), name='listing-list'),
    
]
