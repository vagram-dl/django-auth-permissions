from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
       extra_fields.setdefault('is_active',True)
       extra_fields.setdefault('is_staff',True)
       extra_fields.setdefault('is_superuser',True)

       if extra_fields.get('is_staff') is not True:
           raise ValueError("Суперпользователь должен иметь is_staff=True.")
       if extra_fields.get('is_superuser') is not True:
           raise ValueError("Суперпользователь должен иметь is_superuser=True.")
       return self.create_user(email,password,**extra_fields)



class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    role = models.ForeignKey('Role',on_delete=models.SET_NULL,null=True)
    businesselement = models.ForeignKey(
        "BusinessElement",
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class JWT(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.TextField()
    expire_at = models.DateTimeField()

    def __str__(self):
        return f"JWT for {self.user.email}"

class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

class BusinessElement(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="owned_elements",
        null = True,
        blank = True
    )

    def __str__(self):
        return self.name

class AccessRoleRule(models.Model):
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete = models.CASCADE)

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} -> {self.element}"


# Create your models here.
