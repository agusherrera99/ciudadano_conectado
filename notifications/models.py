from django.db import models

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    issue = models.ForeignKey('issues.Issue', on_delete=models.CASCADE, null=True, blank=True)
    survey = models.ForeignKey('surveys.Survey', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification: #{self.id} - User: {self.user.username}"
    
    class Meta:
        ordering = ('-created_at',)