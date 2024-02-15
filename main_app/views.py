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
      return Agent.objects.all()

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save()
    


class AgentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= Agent.objects.all()
    serializer_class= AgentSerializer
    # might change id to name so the url says name instead of the number will discuss with team perhaps after testing
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Agent.objects.all()

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
        return Listing.objects.all()
    
    
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
      return Agent.objects.all()

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)
    

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset= Client.objects.all()
    serializer_class = ClientSerializer
    # might change this to username will dicuss with the team
    lookup_field = 'id'


    def get_queryset(self):
            # user = self.request.user
            return Client.objects.all()

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

class CreateClientView(generics.CreateAPIView):
  queryset = Client.objects.all()
  serializer_class = ClientSerializer

  def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            client_data = request.data
            client_data['user'] = user.id  # Associate the user with the agent
            client_serializer = ClientSerializer(data=client_data)
            if client_serializer.is_valid(raise_exception=True):
                client_serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_serializer.data,
                    'client': client_serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class LoginClientView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
            try:
                # Query the Client model to get the client associated with the user
                client = Client.objects.get(user=user)
            except Client.DoesNotExist:
                return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'client': ClientSerializer(client).data  # Serialize the client data
            })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    
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
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            agent_data = request.data
            agent_data['user'] = user.id  # Associate the user with the agent
            agent_serializer = AgentSerializer(data=agent_data)
            if agent_serializer.is_valid(raise_exception=True):
                agent_serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_serializer.data,
                    'agent': agent_serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login
class LoginAgentView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      try:
          agent = Agent.objects.get(user=user)
      except Agent.DoesNotExist:
          return Response({'error': 'Client not found'},
          status=status.HTTP_404_NOT_FOUND)
      
      refresh = RefreshToken.for_user(user)
      return Response({
          'refersh': str(refresh),
          'access': str(refresh.access_token),
          'user': UserSerializer(user).data,
          'agent': AgentSerializer(agent).data
      })
    return Response({'errro': 'Indalid Credentils'}, status=status.HTTP_401_UNAUTHORIZED)

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