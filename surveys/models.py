from django.db import models

# Create your models here.
class Survey(models.Model):
    STATUS_CHOICES = (
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pollster = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='pollster', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        self.description = self.description.lower().strip()
        super().save(*args, **kwargs)
    
class Question(models.Model):
    QUESTION_TYPES = (
        ('predefinida', 'Predefinida'),
        ('libre', 'Libre')
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text
    
    def save(self, *args, **kwargs):
        self.question_text = self.question_text.lower().strip()
        super().save(*args, **kwargs)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.option_text
        
    def save(self, *args, **kwargs):
        self.option_text = self.option_text.lower().strip()
        super().save(*args, **kwargs)