from django.db import models


class Restaurant(models.Model):
    """Class that represent an restaurant"""

    name = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"Restaurant {self.name} located in {self.city}."
