from django.db import models

class SystemConfig(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name="Clave")
    value = models.TextField(verbose_name="Valor")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Configuración del sistema"
        verbose_name_plural = "Configuraciones del sistema"
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_value(cls, key, default=None):
        """
        Obtiene el valor de una configuración por su clave.
        Si no existe la configuración, devuelve el valor por defecto.
        """
        try:
            config = cls.objects.get(key=key)
            # Intentar convertir el valor según su contenido
            value = config.value
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            elif value.isdigit():
                return int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                return float(value)
            return value
        except cls.DoesNotExist:
            return default
