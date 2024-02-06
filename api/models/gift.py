from django.core.files.base import ContentFile
from api.models.employee import Employee
from django.db import models
from io import BytesIO
import secrets
import qrcode


class GiftType(models.Model):
    name  = models.CharField(max_length=50)
    mnemo = models.CharField(max_length=10, db_index=True)
    
    class Meta:
        verbose_name = 'gift type'
        verbose_name_plural = "Gift types"
        db_table = "gift_types"

    def __str__(self):
        return self.name
    
class Gift(models.Model):
    label  = models.CharField(max_length=100)
    type = models.ForeignKey(GiftType, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'gift'
        verbose_name_plural = "Gifts"
        db_table = "gifts"
    
    def __str__(self):
        return self.label
    
class GiftEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, blank=True)
    qrcode = models.ImageField(upload_to ='qrcodes/', blank=True) 

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)  # Generate a random API key
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.token)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_file = ContentFile(buffer.getvalue())
            self.qrcode.save(f"{self.token}.png", image_file)
        super(GiftEntry, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'gift entry'
        verbose_name_plural = "Gift Entries"
        db_table = "gift_entries"
    
    def __str__(self):
        return self.gift.label