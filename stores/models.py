from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    open_date = models.DateField()

    def __str__(self):
        return self.name

class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.product_name

class StoreEmployee(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.position})"

class StoreReview(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()


class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventory")
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    restock_date = models.DateField()

    def __str__(self):
        return f"{self.product} - {self.quantity} units"
