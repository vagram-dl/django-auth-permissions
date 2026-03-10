from django.core.management.base import BaseCommand
from permissions.models import User, BusinessElement, AccessRoleRule, Role

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def handle(self, *args, **kwargs):
        print("Запущена новая версия seed_data.py")
        admin_role = Role.objects.create(name="Admin")
        user_role = Role.objects.create(name="User")
        guest_role = Role.objects.create(name="Guest")

        admin_user = User.objects.create(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            is_active=True,
            role=admin_role
        )
        admin_user.set_password("admin123")
        admin_user.save()

        normal_user = User.objects.create(
            first_name="Normal",
            last_name="User",
            email="user@example.com",
            is_active=True,
            role=user_role
        )
        normal_user.set_password("user123")
        normal_user.save()

        guest_user = User.objects.create(
            first_name="Guest",
            last_name="User",
            email="guest@example.com",
            is_active=True,
            role=guest_role
        )
        guest_user.set_password("guest123")
        guest_user.save()

        shop = BusinessElement.objects.create(name="Магазин", owner=admin_user)
        product = BusinessElement.objects.create(name="Товар", owner=normal_user)
        order = BusinessElement.objects.create(name="Заказ", owner=normal_user)

        AccessRoleRule.objects.create(role=admin_role, element=shop, update_all_permission=True)
        AccessRoleRule.objects.create(role=user_role, element=product, update_all_permission=False)
        AccessRoleRule.objects.create(role=guest_role, element=order, update_all_permission=False)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены!"))


# Register your models here.
