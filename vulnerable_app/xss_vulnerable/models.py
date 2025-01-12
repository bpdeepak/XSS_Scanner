from django.db import models

class Comment(models.Model):
    username = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.username
