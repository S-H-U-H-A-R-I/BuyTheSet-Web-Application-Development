import re
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import IntegrityError


# Create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, blank=False)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    
    def __str__(self):
        return self.user.username


# Create a user Profile by default when the user signs up
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            user_profile = Profile(user=instance, email=instance.email)
            user_profile.save()
        except IntegrityError:
            pass

# Automate the creation of a user profile when a user is created
post_save.connect(create_user_profile, sender=User)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'tags'


class Product(models.Model):
    name  = models.CharField(max_length=255, blank=False)
    verbose_name = models.CharField(max_length=255, blank=True)
    cost_price =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/products/', default='no-image.jpg')
    quantity = models.PositiveIntegerField(default=1)
    is_archived = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.verbose_name or self.name != self.__original_name:
            self.verbose_name = re.sub(r'[^\w\s-]', '', self.name.lower().replace(' ', '-'))
        super().save(*args, **kwargs)
        self.__original_name = self.name
    
    @property
    def display_name(self):
        return self.verbose_name or self.name
    
    @property
    def profit(self):
        if self.is_sale:
            return self.sale_price - self.cost_price
        else:
            return self.price - self.cost_price
    
    def serialize_product(self):
        from django.core.serializers import serialize
        import json
        product_dict = json.loads(serialize('json', [self]))[0]
        product_dict['fields']['tags_name'] = [tag.name for tag in self.tags.all()]
        product_dict['fields']['is_archived'] = self.is_archived
        product_dict['fields']['additional_images'] = [image.image.url for image in self.additional_images.all()]
        product_dict['fields']['date_created'] = self.date_created.strftime('%B %d, %Y')
        return product_dict
        

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='uploads/products/', default='no-image.jpg')

    def __str__(self):
        return f"{self.product.name} Additional Image"
    
