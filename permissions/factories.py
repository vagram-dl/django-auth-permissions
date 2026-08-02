from permissions.models import User,Role

class UserFactory:
    @staticmethod
    def create_user(email,password,role_name,first_name="Test",last_name="User",**extra_fields):
        role, _ = Role.objects.get_or_create(name=role_name)

        user = User(
            email = email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active = True,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user