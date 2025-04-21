from django.db import models

class QueryLog(models.Model):
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tone = models.CharField(max_length=50)
    intent = models.CharField(max_length=50)
    suggested_actions = models.JSONField()

    def __str__(self):
        return f"{self.timestamp}: {self.query[:50]}"