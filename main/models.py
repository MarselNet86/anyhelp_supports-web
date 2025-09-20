from django.db import models
from django.conf import settings


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
    
    
    
class FieldSupport(models.Model):
    STATUS_CHOICES = [
        ("processing",  "В обработке"),
        ("accepted",    "Принят"),
        ("rejected",    "Отклонен"),
    ]

    photo   = models.ImageField("Фото", upload_to="field_supports/photos/%Y/%m/", null=True, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    status  = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="processing")
    address = models.TextField("Адрес", blank=True)
    owner = models.CharField("Владеющая организация", max_length=255, blank=True)
    material = models.CharField("Материал несущей конструкции", max_length=100, blank=True)


    latitude  = models.DecimalField("Широта",  max_digits=9,  decimal_places=6, null=True, blank=True,
                                    )
    longitude = models.DecimalField("Долгота", max_digits=9,  decimal_places=6, null=True, blank=True,
                                    )

    # Метаданные
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        related_name="field_supports",
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Полевой объект (опора)"
        verbose_name_plural = "Полевые объекты (опоры)"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return f"Полевой объект #{self.pk} ({self.get_status_display()})"