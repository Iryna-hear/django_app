from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password,  **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not phone_number:
            raise ValueError('Phone number is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, phone_number, password, **extra_fields)
    

    def active_users(self, date):
        return self.filter(is_active=True, date_joined__gte=date)
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Phone Number')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Last Name')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='Profile Picture')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    is_staff = models.BooleanField(default=False, verbose_name='Is Staff')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date Joined')
    preferred_language = models.CharField(max_length=10, choices=[
        ('en', 'English'), 
        ('uk', 'Українська')
    ], default='en', verbose_name='Preferred Language')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    class Meta:
      verbose_name = 'User'
      verbose_name_plural = 'Users'
      permissions = [
          ('can_view_profile', 'Can view profile'),
          ('can_edit_profile', 'Can edit profile'),
          ('can_delete_profile', 'Can delete profile'),
      ]


    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    

class UserAdress(models.Model):
        user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='address')
        street = models.CharField(max_length=255, verbose_name='Street')
        city = models.CharField(max_length=100, verbose_name='City')
        postal_code = models.CharField(max_length=20, verbose_name='Postal Code')
        country = models.CharField(max_length=100, verbose_name='Country')
        
        class Meta:
            verbose_name = 'User Address'
            verbose_name_plural = 'User Addresses'
        
        def __str__(self):
            return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"
        
class UserPayment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Payment Date')
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer')
    ], default='credit_card', verbose_name='Payment Method')
    

    
    def __str__(self):
        return f"Payment info for {self.user.email} - {self.amount}"
        

