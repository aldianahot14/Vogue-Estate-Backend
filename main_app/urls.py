from django.urls import path
from .views import Home, AgentList, AgentDetails, AgentListingsList, AgentListingsDetails, ListingList, ClientList, ClientDetail, CreateUserView, LoginView, VerifyUserView, CreateAgentView, VerifyAgentView, LoginAgentView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('agents/', AgentList.as_view(), name='property-list'),
    path('agentdetails/<int:id>/', AgentDetails.as_view(), name='agent-detail'),
    path('agentlisting/<int:agent_id>/', AgentListingsList.as_view(), name='agent-list'),
    path('agentlistingdetails/<int:id>/', AgentListingsDetails.as_view(), name='agent-listing-details'),
    path('listinglist/', ListingList.as_view(), name='listing-list'),
    path('clientlist/', ClientList.as_view(), name='client-list'),
    path('clientdetail/<int:id>/', ClientDetail.as_view(), name='client-detail'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('agents/token/refresh/', VerifyAgentView.as_view(), name='token_refresh'),
    path('agents/register/', CreateAgentView.as_view(), name='register'),
    path('agents/login/', LoginAgentView.as_view(), name='login'),
    
    
]
