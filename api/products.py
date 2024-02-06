from api.models.products import ProductType, ProductEntry, Product
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from api.models.employee import Employee
from rest_framework import serializers

class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ['id', 'name', 'mnemo']

class ProductSerializer(serializers.ModelSerializer):
    type__id = serializers.IntegerField(source='type.id')
    type__name = serializers.CharField(source='type.name')
    type__mnemo = serializers.CharField(source='type.mnemo')

    class Meta:
        model = Product
        fields = ['id', 'label', 'type__id', 'type__name', 'type__mnemo']

class ProductEntrySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all())
    employee = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Employee.objects.all())
    employee__id = serializers.IntegerField(source='employee.id', read_only=True)
    employee__points = serializers.IntegerField(source='employee.points', read_only=True)
    user__id = serializers.IntegerField(source='employee.user.id', read_only=True)
    user__first_name = serializers.CharField(source='employee.user.first_name', read_only=True)
    user__last_name = serializers.CharField(source='employee.user.last_name', read_only=True)
    user__username = serializers.CharField(source='employee.user.username', read_only=True)
    user__email = serializers.CharField(source='employee.user.email', read_only=True)
    product__label = serializers.CharField(source='product.label', read_only=True)
    product__type__id = serializers.IntegerField(source='product.type.id', read_only=True)
    product__type__name = serializers.CharField(source='product.type.name', read_only=True)
    product__type__mnemo = serializers.CharField(source='product.type.mnemo', read_only=True)

    def validate(self, data):
        employee = data.get('employee')

        if employee.user != self.context['request'].user:
            raise serializers.ValidationError("You're not allowed to peform this action.")
        
        return data

    def create(self, data):
        employee = data.get('employee')
        product = data.get('product')
        employee.points += product.points
        
        return data
        
    class Meta:
        model = ProductEntry
        fields = ['id', 'product', 'employee','employee__id','employee__points','user__id',
                  'user__first_name','user__last_name','user__username','user__email',
                  'product__label','product__type__id','product__type__name', 'product__type__mnemo'
                  ]
        read_only_fields = ['id', 'employee__id','employee__points','user__id',
                  'user__first_name','user__last_name','user__username','user__email',
                  'product__label','product__type__id','product__type__name', 'product__type__mnemo'
                  ]

class ProductTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductTypeSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

class ProductEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductEntry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductEntrySerializer

class ProductEntryAddView(generics.CreateAPIView):
    queryset = ProductEntry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductEntrySerializer
    