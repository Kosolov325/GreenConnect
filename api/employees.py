from rest_framework.permissions import IsAuthenticated
from api.models.employee import Employee
from rest_framework import serializers
from rest_framework import viewsets

class EmployeeSerializer(serializers.ModelSerializer):
    user__id = serializers.IntegerField(source='user.id')
    user__first_name = serializers.CharField(source='user.first_name')
    user__last_name = serializers.CharField(source='user.last_name')
    user__username = serializers.CharField(source='user.username')
    user__email = serializers.CharField(source='user.email')

    class Meta:
        model = Employee
        fields = ['id', 'user__id', 'user__first_name', 'user__last_name', 'user__username', 'user__email', 'points']
    
class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer