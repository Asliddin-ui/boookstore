from django.db import models


class Language(models.Model):
    lang = models.CharField(max_length=25)


class Country(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Category', on_delete=models.RESTRICT, blank=True, null=True)


class Authors(models.Model):
    name = models.CharField(max_length=120)


class Books(models.Model):
    STATUS_NEW = 0
    STATUS_PUBLISHED = 1
    STATUS_REJECTED = 2


    name = models.CharField(max_length=255)
    content = models.TextField()

    authors = models.ManyToManyField(Authors)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.ImageField(upload_to='books_photos')
    status = models.IntegerField(choices=(
        (STATUS_NEW, 'Yangi'),
        (STATUS_PUBLISHED, 'Qabul qilingan'),
        (STATUS_REJECTED, 'Inkor qiligan')
    ))
    rating_stars = models.IntegerField()
    rating_count = models.IntegerField()
    availability = models.BooleanField(default=False)
    read = models.IntegerField()
    reading = models.IntegerField()
    will_read = models.IntegerField()
    publish_year = models.IntegerField(blank=True, null=True, default=None)
    added_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)