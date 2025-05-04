from rest_framework import viewsets, permissions, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Habit, HabitLog
from .serializers import HabitSerializer, CategorySerializer, HabitLogSerializer, RegisterSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category_name']
    ordering = ['id']  # Чтобы не было предупреждения пагинации при формировании всех объектов,
    # так как для пагинации может быть важен порядок, чтобы не было дублирования. Используется OrderingFilter и ordering
    # иначе придется писать queryset = Hotel.objects.all().order_by('id')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Только админ может создавать, изменять, удалять
        return [permissions.AllowAny()]  # Пользователь может только смотреть


class HabitLogViewSet(viewsets.ModelViewSet):
    queryset = HabitLog.objects.all()
    serializer_class = HabitLogSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = 'user', 'habit'
    search_fields = ['habit', 'execute_date']
    ordering = ['id']  # Чтобы не было предупреждения пагинации при формировании всех объектов,
    # так как для пагинации может быть важен порядок, чтобы не было дублирования. Используется OrderingFilter и ordering
    # иначе придется писать queryset = Hotel.objects.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        return [permissions.IsAuthenticated()]


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['habit_name', 'category', 'period']
    ordering = ['id']  # Чтобы не было предупреждения пагинации при формировании всех объектов,
    # так как для пагинации может быть важен порядок, чтобы не было дублирования. Используется OrderingFilter и ordering
    # иначе придется писать queryset = Hotel.objects.all().order_by('id')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Только админ может создавать, изменять, удалять
        return [permissions.AllowAny()]  # Пользователь может только смотреть



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        created_user = user.save()
        refresh = RefreshToken.for_user(created_user)
        return Response({
            "user": user.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
