from django.db import models
from django.db.models import Q
from accounts.custom_models.choices import StatusChoices
PROVINCE_MAP = {
    "KZN": "KwaZulu-Natal",
    "MP": "Mpumalanga",
    "NW": "North-West",
    "FS": "Free-State",
    "WC": "Western Cape",
    "LP": "Limpopo",
    "GP": "Gauteng",
    "EC": "Eastern Cape",
    "NC": "Northern Cape",
}
class BusinessManager(models.Manager):

    def by_province(self, province:str):
        province = province.strip()

        # User supplied code (GP)
        if province.upper() in PROVINCE_MAP:
            code = province.upper()
            name = PROVINCE_MAP[code]

        # User supplied full name (Gauteng)
        else:
            code = next(
                (k for k, v in PROVINCE_MAP.items()
                 if v.lower() == province.lower()),
                None
            )
            name = province

        return self.filter(
            Q(province=code) |
            Q(main_address__icontains=name)
        ).distinct()

    def approved_by_province(self, province):
        province = province.strip()

        # User supplied code (GP)
        if province.upper() in PROVINCE_MAP:
            code = province.upper()
            name = PROVINCE_MAP[code]

        # User supplied full name (Gauteng)
        else:
            code = next(
                (k for k, v in PROVINCE_MAP.items()
                 if v.lower() == province.lower()),
                None
            )
            name = province

        return self.filter(
            Q(province=code) |
            Q(main_address__icontains=name)
        ).distinct().filter(status=StatusChoices.APPROVED)