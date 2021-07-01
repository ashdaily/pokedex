from django.db import models


class Pokemon(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Pokemon\'s Name"
    )
    description = models.TextField(
        max_length=500, 
        help_text="Pokemon\'s Description"
    )
    habitat = models.CharField(
        max_length=255, 
        help_text="Pokemon\'s Habitat"
    )
    is_legendary = models.BooleanField(
        default=False, 
        help_text="Pokemon\'s is_legendary status"
    )
    
    def __str__(self):
        return f"{self.id} : {self.name}"
    




