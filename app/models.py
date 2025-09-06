from django.db import models

class Slate(models.Model):
    slate_guid = models.CharField(max_length=20)
    bu_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.slate_guid} - {self.bu_id}"
