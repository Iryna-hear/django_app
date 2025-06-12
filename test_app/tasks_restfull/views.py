from rest_framework import viewsets, filters, status
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from tasks.models import Task
from tasks_restfull.serializers import TaskSerializer
from tasks_restfull.authentication import CustomTokenAuthentication, CustomJWTAuthentication
from tasks_restfull.utils import create_token_for_user, generate_jwt_token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'user']
    search_fields = ['title', 'descriptions']
    ordering_fields = ['created_at', 'completed']
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()

class TaskReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'user']


class TaskGenerViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'user']
    search_fields = ['title', 'descriptions']
    ordering_fields = ['created_at', 'completed']

    def perform_create(self, serializer):
        serializer.save()
    
class TaskCustomViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Task.objects.filter(completed=False)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
class TaskCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskUpdateViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})
    
@api_view(['POST'])
@permission_classes([])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user:
        token = create_token_for_user(user)
        return Response({
            'token': token.key, 
            'user_id': user.pk, 
            'expires_at': token.expires_at,
            'email': user.email}, 
            status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([])
def login_jwt(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user:
        token = generate_jwt_token(user)
        return Response({
            'access_key': token, 
        })
    return Response({'error': 'Invalid credentials'}, status=401)

