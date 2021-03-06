from django.db import models

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import uuid

class Journal(models.Model):
    """Model representing a journal."""
    name = models.CharField(max_length=200, help_text='Enter a journal name (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Author(models.Model):
    "Model representing the author of an publication"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.last_name

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Edition(models.Model):
    """Model representing an edition of a journal"""

    number = models.IntegerField(help_text='Number of the edition')
    year = models.IntegerField(help_text='Year of the edition', validators=[MinValueValidator(0),
                                       MaxValueValidator(datetime.date.today().year+1)])
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return (str(self.journal) + ", " + str(self.year) + ", " + str(self.number) + " edition")

class Publication(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular publication')
    title = models.CharField(max_length=200)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.SET_NULL, null=True)
    text = models.TextField(help_text='Text of the publication')
    date = models.DateField(auto_now_add = True, help_text='Date when publication was published')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('publication-detail', args=[str(self.id)])
