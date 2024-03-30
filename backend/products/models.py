from django.conf import settings
from django.db import models
from django.db.models import Q
import random
from rest_framework.reverse import reverse

User = settings.AUTH_USER_MODEL
PRODUCTS_TAGS = ['cars', 'electronics', 'toys', 'fun']
 
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        #this is a new method for our custom qs
        return self.filter(public=True)
    
    def search(self, query, user=None):
        #searching logic
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup) #if the user is not authenticated they he can view public data only
        if user is not None:
            if user.is_superuser: #if the user is admin then he can access the private data also
                return self.filter(lookup)
            
            qs2 = self.filter(user=user).filter(lookup) #this will filter all the items which are owned by an user
            qs = (qs | qs2).distinct() #this will combine the distinct results from qs and qs2 -> public data + user 
                                                                                        # owned data which can be private
        return qs

## making a custom manager to handle search query
class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #overriding the queryset
        return ProductQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, default=99.99, decimal_places=2)
    public = models.BooleanField(default=True)
    
    objects = ProductManager()
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.id})
    
    @property
    def endpoint(self):
        return self.get_absolute_url()
    
    def is_public(self): #for algoliasearch
        ## run reindex again, for algolia, if this method is changed 
        return self.public
    
    def get_tags(self):
        return [random.choice(PRODUCTS_TAGS)]
    
    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    
    @property
    def path(self):
        return f"/products/{self.pk}"
    
    @property
    def body(self):
        return self.content
    
    def get_discount(self):
        return "122"