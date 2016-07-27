from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django_extras.contrib.auth.models import SingleOwnerMixin

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
    shattered = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Listing(SingleOwnerMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(help_text="Million ISK")
    notes = models.TextField(blank=True, null=True)

    sold = models.DateTimeField(blank=True, null=True)

    def mark_sold(self):
        self.sold = timezone.now()
        self.save()

    @property
    def raw_price(self):
        return self.price * 1000000

    def __str__(self):
        return "%s - %s" % (self.owner, self.system)

@python_2_unicode_compatible
class Wanted(SingleOwnerMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, blank=True, null=True)
    wormhole_class = models.PositiveIntegerField(blank=True, null=True)
    _statics = models.ManyToManyField(Wormhole, blank=True)
    effect = models.ManyToManyField(Effect, blank=True)
    shattered = models.BooleanField(default=False, blank=True)
    offering = models.PositiveIntegerField(help_text="Million ISK")
    notes = models.TextField(blank=True, null=True)

    fulfilled = models.DateTimeField(blank=True, null=True)

    def mark_fulfilled(self):
        self.fulfilled = timezone.now()
        self.save()

    @property
    def statics(self):
        return list(set([s.destination for s in self._statics.all()]))

    @property
    def raw_offering(self):
        return self.offering * 1000000

    def __str__(self):
        return "%s - %s" % (self.owner, self.created)
