from django.contrib.auth.models import Group, Permission


def create_group(group_name: str, app_label: str, model_name: str, codenames: list):
    """
    Función para crear un grupo y asignarle permisos específicos.
    """

    def create_group_migration(apps, schema_editor):
        try:
            group, created = Group.objects.get_or_create(name=group_name)

            for codename in codenames:
                try:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f'Permiso "{codename}" no encontrado.')

            print(f'Grupo "{group_name}" creado con éxito.')
        except Exception as e:
            print(f'Error al crear el grupo "{group_name}": {e}')

    return create_group_migration
