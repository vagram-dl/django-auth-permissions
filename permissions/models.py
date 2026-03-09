from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    role = models.ForeignKey('Role',on_delete=models.SET_NULL, null=True)

    def set_password(self, raw_password):
        self.password_hash= make_password(raw_password)

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
    name = models.CharField(max_length=100,unique=True)
    owner = models.ForeignKey('User',on_delete=models.CASCADE,null=True,blank=True)

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
