from django.contrib import admin

from .models import Product
from .models import Contact,Orders,OrderUpadate,Registration

admin.site.register(Product),
admin.site.register(Contact),
admin.site.register(Orders),
admin.site.register(OrderUpadate),
admin.site.register(Registration)


