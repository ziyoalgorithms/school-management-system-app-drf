from django.db import models


class Payment(models.Model):
    student = models.ForeignKey('staffs.Student', related_name='payment', on_delete=models.SET_NULL, null=True, blank=True)
    payed_for = models.ForeignKey('lesson.Subject', related_name='payed_for', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.payed_for} fani uchun {self.date} da {self.payed_for.price} so'm to'landi"