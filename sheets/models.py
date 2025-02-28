from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username

class Spreadsheet(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Link to Profile
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} - {self.profile.user.username}"

class Cell(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Sheet: {self.spreadsheet.name} - Row: {self.row}, Col: {self.col}"
