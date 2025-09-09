from django.db import models

class Support(models.Model):
    settlement = models.CharField("Населённый пункт", max_length=255)
    branch = models.CharField("Филиал", max_length=255)
    support_number = models.CharField("Номер опоры", max_length=50)
    name = models.CharField("Название опоры", max_length=255, blank=True)
    address = models.TextField("Адрес", blank=True)
    longitude = models.DecimalField("Долгота", max_digits=15, decimal_places=10, null=True, blank=True)
    latitude = models.DecimalField("Широта", max_digits=15, decimal_places=10, null=True, blank=True)
    commissioning_date = models.DateTimeField("Дата ввода в эксплуатацию", null=True, blank=True)
    owner = models.CharField("Владеющая организация", max_length=255, blank=True)
    material = models.CharField("Материал несущей конструкции", max_length=100, blank=True)
    photo = models.ImageField("Фото", upload_to="supports/photos/", null=True, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    
    STATUS_CHOICES = [
        ("accepted", "Принят"),
        ("processing", "В обработке"),
        ("rejected", "Отклонен"),
        ("not_started", "Не начат")
    ]
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="not_started")

    class Meta:
        verbose_name = "Опора"
        verbose_name_plural = "Опоры"
        ordering = ["settlement", "support_number"]

    def __str__(self):
        return f"{self.name or 'Опора'} №{self.support_number} ({self.settlement})"