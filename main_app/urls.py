from django.urls import path
from .views import Home, AgentList, AgentDetails, AgentListingsList, AgentListingsDetails, ListingList, ClientList, ClientDetail, CreateUserView, LoginView, VerifyUserView, CreateAgentView, VerifyAgentView, LoginAgentView, CreateClientView

urlpatterns = [
    # home
    path('', Home.as_view(), name='home'),
    # brings up list of all agents and their listings
    path('agents/', AgentList.as_view(), name='property-list'),
    # brings up list of all listings for that agent and their info via the agent id
    path('agentdetails/<int:id>/', AgentDetails.as_view(), name='agent-detail'),
    # brings up list of agents listings
    path('agentlisting/<int:agent_id>/', AgentListingsList.as_view(), name='agent-list'),
    # brings up that particular listing and all its details, ask aldiana if we can rename it 
    path('agentlistingdetails/<int:id>/', AgentListingsDetails.as_view(), name='agent-listing-details'),
    # brings up list of all listings
    path('listinglist/', ListingList.as_view(), name='listing-list'),
    # brings up list of all clients
    path('clientlist/', ClientList.as_view(), name='client-list'),
    # returns particular client details
    path('clientdetail/<int:id>/', ClientDetail.as_view(), name='client-detail'),
    # this works but not sure it's needed 
    path('users/register/', CreateUserView.as_view(), name='register'),
    # this works but not sure it's needed
    path('users/login/', LoginView.as_view(), name='login'),
    # this works but not sure it's needed
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    # works
    path('agents/token/refresh/', VerifyAgentView.as_view(), name='token_refresh'),
    # works
    path('agents/register/', CreateAgentView.as_view(), name='register'),
    # works
    path('agents/login/', LoginAgentView.as_view(), name='login'), 
    # works
    path('client/register/', CreateClientView.as_view(), name='register'),
    
]
