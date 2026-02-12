from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

class Film(models.Model):
    slug = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    
    is_checked_in = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate QR code when saving
        if not self.qr_code:
            qr_data = str(self.id)
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            fname = f'qr_{self.user.mobile_number}_{self.film.slug}.png'
            self.qr_code.save(fname, File(buffer), save=False)
            
        super().save(*args, **kwargs)