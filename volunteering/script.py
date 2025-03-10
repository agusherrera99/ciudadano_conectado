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