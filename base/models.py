from django.db import models

# Create your models here.
#products table
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default="")
    subcategory = models.CharField(max_length=100,default="")
    price  = models.IntegerField(default=0)
    description = models.CharField(max_length=300,default="")
    publish_date = models.DateField()
    image = models.ImageField(upload_to='shop/images',default="")
    
    def __str__(self):
        return self.product_name
    
# orders table
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=10000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    email = models.EmailField(default="client@gmail.com")
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    # extra fields to update dynamically 
    iod = models.CharField(max_length=300,blank=True)
    amountpaid = models.CharField(max_length=300,blank=True,null=True)
    paymentstatus= models.CharField(max_length=300)
    
    phone = models.CharField(max_length=15,default="")
    def __str__(self):
        return self.name
    
# orders update table for tracking items
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        # slicing description
        return self.update_desc[0:9] + "..."
    
