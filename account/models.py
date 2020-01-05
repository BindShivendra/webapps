from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractUser

from PIL import Image

class UserManager(BaseUserManager):
    use_in_migrations = True


    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_employee(self):
        return self.is_active and ( self.is_superuser 
                or self.is_staff and self.groups.filter(name='Employees').exists()
            )

    @property
    def username(self):
        return f'{self.first_name} {self.last_name}'



class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics/%Y/%m/%d')

    def __str__(self):
        return self.profile.username

    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)

        img = Image.open(self.profile_pic.path)
        # img = img.convert('RGB')
        if img.height > 300 or img.width > 300:
            out_size = (300,300)
            img.thumbnail(out_size)
            img = img.convert('RGB')
            img.save(self.profile_pic.path)