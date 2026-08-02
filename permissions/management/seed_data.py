from tkinter.font import names

from django.core.management.base import BaseCommand
from permissions.models import User,BusinessElement,AccessRoleRule,Role
from permissions.factories import UserFactory

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"
    def handle(self, *args, **kwargs):
        self.stdout.write("Запущено заполнение тестовыми данными...")

        admin_role, _ = Role.objects.get_or_create(name="Admin")
        user_role, _ = Role.objects.get_or_create(name="User")
        guest_role, _ = Role.objects.get_or_create(name="Guest")
        self.stdout.write("Создание тестовых пользователей...")

        UserFactory.create_user(
            email="admin@example.com",
            password="admin123",
            role_name="Admin",
            first_name="Главный",
            last_name="Админ"
        )


        UserFactory.create_user(
            email="user@example.com",
            password="user123",
            role_name="User",
            first_name="Обычный",
            last_name="Пользователь"
        )

        orders_element, _ = BusinessElement.objects.get_or_create(name='Orders')
        users_element, _ = BusinessElement.objects.get_or_create(name='Users')

        AccessRoleRule.objects.get_or_create(
            role = admin_role,
            element = orders_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True
            }
        )

        AccessRoleRule.objects.get_or_create(
            role=user_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                'create_permission': False,
                'update_permission': False,
                'update_all_permission': False,
                'delete_permission': False,
                'delete_all_permission': False
            }
        )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми данными!'))
        self.stdout.write(self.style.WARNING('Тестовые доступы: admin@example.com / admin123, user@example.com / user123')