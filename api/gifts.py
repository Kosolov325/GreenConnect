from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status
from api.models.gift import GiftType, Gift, GiftEntry
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.employee import Employee
from rest_framework import serializers
import numpy as np
import cv2


class GiftTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftType
        fields = ['id', 'name', 'mnemo']

class GiftSerializer(serializers.ModelSerializer):
    type__id = serializers.IntegerField(source='type.id')
    type__name = serializers.CharField(source='type.name')
    type__mnemo = serializers.CharField(source='type.mnemo')

    class Meta:
        model = Gift
        fields = ['id', 'label', 'type__id', 'type__name', 'type__mnemo']

class GiftEntrySerializer(serializers.ModelSerializer):
    gift = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Gift.objects.all())
    employee = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Employee.objects.all())
    employee__id = serializers.IntegerField(source='employee.id', read_only=True)
    employee__points = serializers.IntegerField(source='employee.points', read_only=True)
    user__id = serializers.IntegerField(source='employee.user.id', read_only=True)
    user__first_name = serializers.CharField(source='employee.user.first_name', read_only=True)
    user__last_name = serializers.CharField(source='employee.user.last_name', read_only=True)
    user__username = serializers.CharField(source='employee.user.username', read_only=True)
    user__email = serializers.CharField(source='employee.user.email', read_only=True)
    gift__label = serializers.CharField(source='gift.label', read_only=True)
    gift__type__id = serializers.IntegerField(source='gift.type.id', read_only=True)
    gift__type__name = serializers.CharField(source='gift.type.name', read_only=True)
    gift__type__mnemo = serializers.CharField(source='gift.type.mnemo', read_only=True)

    def validate(self, data):
        employee = data.get('employee')
        gift = data.get('gift')

        if employee.user != self.context['request'].user or employee.points < gift.price:
            raise serializers.ValidationError("You're not allowed to peform this action.")
        
        return data

    def create(self, data):
        employee = data.get('employee')
        gift = data.get('gift')
        employee.points -= gift.price
        
        return data
        
    class Meta:
        model = GiftEntry
        fields = ['id', 'gift', 'employee','employee__id','employee__points','user__id',
                  'user__first_name','user__last_name','user__username','user__email',
                  'gift__label','gift__type__id','gift__type__name', 'gift__type__mnemo',
                  'token', 'qrcode'
                  ]
        read_only_fields = ['id', 'employee__id','employee__points','user__id',
                  'user__first_name','user__last_name','user__username','user__email',
                  'gift__label','gift__type__id','gift__type__name', 'gift__type__mnemo',
                  'token', 'qrcode'
                  ]

class GiftTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GiftType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GiftTypeSerializer

class GiftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gift.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GiftSerializer

class GiftEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GiftEntry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GiftEntrySerializer

class GiftEntryAddView(generics.CreateAPIView):
    queryset = GiftEntry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GiftEntrySerializer

class GiftValidate(APIView):
    queryset = GiftEntry.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            memory_file = request.data['file']
            nparr = np.fromstring(memory_file.file.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            qcd = cv2.QRCodeDetector()
            retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
            gift = GiftEntry.objects.get(token=decoded_info[0])
            return Response(GiftEntrySerializer(gift).data,status=status.HTTP_202_ACCEPTED)   
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)   
        except GiftEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        

    