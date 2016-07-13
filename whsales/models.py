from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django_extras.contrib.auth.models import SingleOwnerMixin
from whsales.managers import UserManager

@python_2_unicode_compatible
class Wormhole(models.Model):
    DESTINATION_CHOICES = (
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('Class 5', 'Class 5'),
        ('Class 6', 'Class 6'),
        ('Class 13', 'Class 13'),
        ('High-Sec', 'High-Sec'),
        ('Low-Sec', 'Low-Sec'),
        ('Null-Sec', 'Null-Sec'),
        ('Thera', 'Thera'),
        ('Barbican', 'Barbican'),
        ('Conflux', 'Conflux'),
        ('Redoubt', 'Redoubt'),
        ('Sentinel', 'Sentinel'),
        ('Vidette', 'Vidette'),
    )

    name = models.CharField(max_length=4, primary_key=True)
    lifetime = models.PositiveIntegerField()
    mass = models.PositiveIntegerField()
    jumpable = models.PositiveIntegerField()
    destination = models.CharField(max_length=8, choices=DESTINATION_CHOICES)
    regenerate = models.BooleanField(default=False)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Effect(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class System(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=7)
    wormhole_class = models.PositiveIntegerField()
    effect = models.ForeignKey(Effect, blank=True, null=True, on_delete=models.SET_NULL)
    statics = models.ManyToManyField(Wormhole, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    character_id = models.PositiveIntegerField(primary_key=True)
    character_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'character_name'
    REQUIRED_FIELDS = ['character_id']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.get_short_name() + " (%s)" % self.character_id
    def get_short_name(self):
        return str(self.character_name)

    def __str__(self):
        return self.get_short_name()

@python_2_unicode_compatible
class Listing(SingleOwnerMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    sold = models.DateTimeField(blank=True, null=True)

    def mark_sold(self):
        self.sold = timezone.now()
        self.save()

    def __str__(self):
        return "%s - %s" % (self.owner, self.system)
