from django.db import models
from django.contrib.auth.models import User
from datetime import date
#******************************************************************#
# Create your models here.
class Itemtype(models.Model):
    """Model representing item type."""
    name = models.CharField(max_length=200, help_text='Enter an item type (e.g. Electronics or mechanical)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
#******************************************************************#
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Item(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the item')
    #isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    itemtype = models.ManyToManyField(Itemtype, help_text='Select an item type for this item')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this item."""
        return reverse('item-detail', args=[str(self.id)])
#******************************************************************#
import uuid # Required for unique book instances

class ItemInstance(models.Model):
    """Model representing a specific copy of an item (i.e. that can be borrowed from the inventory)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular item across whole inventory')
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    #imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Item availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set item as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.item.title})'

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

#******************************************************************#
class Manufacturer(models.Model):
    """Model representing an author."""
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    #date_of_birth = models.DateField(null=True, blank=True)
    #date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['company_name', 'address']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('manufacturer-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.company_name}, {self.address}'
#******************************************************************#
from django.forms import ModelForm

from catalog.models import ItemInstance

# class RenewItemModelForm(ModelForm):
#     def clean_due_back(self):
#        data = self.cleaned_data['due_back']
#
#        # Check if a date is not in the past.
#        if data < datetime.date.today():
#            raise ValidationError(_('Invalid date - renewal in past'))
#
#        # Check if a date is in the allowed range (+4 weeks from today).
#        if data > datetime.date.today() + datetime.timedelta(days=4):
#            raise ValidationError(_('Invalid date - renewal more than 4 days ahead'))
#
#        # Remember to always return the cleaned data.
#        return data
#     class Meta:
#         model = ItemInstance
#         fields = ['due_back']
#         labels = {'due_back': _('New renewal date')}
#         help_texts = {'due_back': _('Enter a date between now and 4 days (default 3).')}
#******************************************************************#

#******************************************************************#
