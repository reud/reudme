from django.db import models
from django.utils import timezone


# Create your models here.
class Vocabulary(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    author_line_id = models.CharField(null=True, blank=True)
    serif = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    use_time = models.DateTimeField()
    STATE = (
        ('SENDED', '送信済み'),
        ('WAITING', '未送信'),
        ('DRAFT', '下書き'),
    )
    state = models.CharField(max_length=1, choices=STATE)

    def __str__(self):
        return self.serif
