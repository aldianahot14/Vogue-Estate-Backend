from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics, status, permissions # modify these imports to match
from .models import Agent, Client, Listing, ListingImage
from .serialzers import AgentSerializer, ClientSerializer, AgentListingsSerializer, ListingSerializer, UserSerializer

# include the following imports
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.exceptions import PermissionDenied # include this additional import


# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Vougue Estate home route!'}
        return Response(content)
    
class AgentList(generics.ListCreateAPIView):
    serializer_class= AgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Agent.objects.filter(user=user)

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)


class AgentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= Agent.objects.all()
    serializer_class= AgentSerializer
    # might change id to name so the url says name instead of the number will discuss with team perhaps after testing
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Agent.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        listings_not_associated = Listing.objects.exclude(id__in=instance.listings.all())
        Listing_serializer = ListingSerializer(listings_not_associated, many=True)

        return Response({
            'client': serializer.data,
            'listings_not_associated': Listing_serializer.data
        })

    def perform_update(self, serializer):
        agent = self.get_object()
        if agent.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this listing."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this listing."})
        instance.delete()

class AgentListingsList(generics.ListCreateAPIView):
    serializer_class= AgentListingsSerializer 

    def get_queryset(self):
        # might change to agent name will discuss with team perhaps after testing 
        agent_id= self.kwargs['agent_id']
        return Listing.objects.filter(agent_id=agent_id)
    
    # def perform_create(self, serializer):
    #     agent_id = self.kwargs['agent_id']
    #     agent = Agent.objects.get(id=agent_id)
    #     listing = serializer.save(agent=agent)


    #     images_data = self.request.data.get('images')
    #     for image_data in images_data:
    #         ListingImage.objects.create(property=listing, image=image_data['image'])



class AgentListingsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentListingsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        agent_id = self.kwargs['id']
        return Listing.objects.filter(agent_id = agent_id)
    
    
class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()




class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Agent.objects.filter(user=user)

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)
    

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Client.objects.all()
    serializer_class = ClientSerializer
    # might change this to username will dicuss with the team
    lookup_field = 'id'


    def get_queryset(self):
            user = self.request.user
            return Client.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response({
                'client': serializer.data,
               
            })

    def perform_update(self, serializer):
            agent = self.get_object()
            if agent.user != self.request.user:
                raise PermissionDenied({"message": "You do not have permission to edit this profile."})
            serializer.save()

    def perform_destroy(self, instance):
            if instance.user != self.request.user:
                raise PermissionDenied({"message": "You do not have permission to delete this profile."})
            instance.delete()


    
# include the registration, login, and verification views below
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  

  # include the registration, login, and verification views below
# User Registration
class CreateAgentView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginAgentView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyAgentView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })