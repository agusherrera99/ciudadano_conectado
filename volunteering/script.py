def init_days(apps, schema_editor):
    Day = apps.get_model("volunteering", "Day")

    
    days = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábados",
        "Domingos"
    ]

    for day_name in days:
        Day.objects.create(name=day_name)

def init_categories(apps, schema_editor):
    VolunteerCategory = apps.get_model("volunteering", "VolunteerCategory")

    categories = [
        "medio ambiente",
        "social",
        "educación",
        "salud",
        "cultura",
        "comunitario",
        "deporte"
    ]

    for category_name in categories:
        VolunteerCategory.objects.create(name=category_name)