from django.core.management.base import BaseCommand
from permissions.models import User,BusinessElement,AccessRoleRule,Role

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"
    def handle(self, *args, **kwargs):
        self.stdout.write("Запущено заполнение тестовыми данными...")

        admin_role, _ = Role.objects.get_or_create(name="Admin")
        user_role, _ = Role.objects.get_or_create(name="User")
        guest_role, _ = Role.objects.get_or_create(name="Guest")
        self.stdout.write("Роли созданы")

        admin_user, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={"first_name": "Admin", "last_name": "User", "is_active": True, "role": admin_role}
        )
        admin_user.set_password("admin123")
        admin_user.save()

        normal_user, _ = User.objects.get_or_create(
            email="user@example.com",
            defaults={"first_name": "Normal", "last_name": "User", "is_active": True, "role": user_role}
        )
        normal_user.set_password("user123")
        normal_user.save()

        guest_user, _ = User.objects.get_or_create(
            email="guest@example.com",
            defaults={"first_name": "Guest", "last_name": "User", "is_active": True, "role": guest_role}
        )

        guest_user.set_password("guest123")
        guest_user.save()
        self.stdout.write("Пользователи созданы")

        shop, _ = BusinessElement.objects.get_or_create(name="Магазин", defaults={"owner": admin_user})
        product, _ = BusinessElement.objects.get_or_create(name="Товар", defaults={"owner": normal_user})
        order, _ = BusinessElement.objects.get_or_create(name="Заказ", defaults={"owner": normal_user})
        self.stdout.write("Бизнес-элементы созданы")
        AccessRoleRule.objects.get_or_create(
            role=admin_role, element=shop,
            defaults={"update_all_permission": True}
        )
        AccessRoleRule.objects.get_or_create(
            role=user_role, element=product,
            defaults={"update_all_permission": False}
        )
        AccessRoleRule.objects.get_or_create(
            role=guest_role, element=order,
            defaults={"update_all_permission": False}
        )

        self.stdout.write("Правила доступа созданы")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены!"))
        self.stdout.write(self.style.WARNING("Данные для входа:"))
        self.stdout.write("Admin: admin@example.com / admin123")
        self.stdout.write("User: user@example.com / user123")
        self.stdout.write("Guest: guest@example.com / guest123\n")