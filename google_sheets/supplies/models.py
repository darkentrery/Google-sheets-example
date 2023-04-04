from django.db import models

from django.utils.translation import gettext_lazy as _


class Supply(models.Model):
    number = models.IntegerField(_("Number"), unique=True)
    order = models.IntegerField(_("Order"))
    cost = models.FloatField(_("Cost"))
    date = models.DateField(_("Date of supply"))
    cost_rub = models.FloatField(_("Cost in RUB"))

    class Meta:
        verbose_name = "Supply"
        verbose_name_plural = "Supplies"
        ordering = ["number",]

    def __str__(self):
        return f"{self.number} - {self.order}"
