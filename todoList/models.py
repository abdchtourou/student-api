from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from student.models import Student

class Todo(models.Model):
    """Todo model representing a task to be completed by a student.
    
    Each todo is associated with a student and includes task details,
    completion status, and timestamps for tracking.
    """
    # Relationships
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='todos',
        verbose_name=_('Student'),
        help_text=_('The student who owns this task')
    )
    
    # Core fields
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Title'),
        help_text=_('Title of the task (3-100 characters)')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Optional detailed description of the task')
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Completed'),
        help_text=_('Whether the task has been completed')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
        help_text=_('When the task was created')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
        help_text=_('When the task was last updated')
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Deleted at'),
        help_text=_('When the task was soft deleted')
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Is deleted'),
        help_text=_('Whether the task has been soft deleted')
    )
    
    class Meta:
        """Meta options for the Todo model."""
        verbose_name = _('Todo')
        verbose_name_plural = _('Todos')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', '-created_at']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        """Return a string representation of the todo."""
        return self.title
        
    def clean(self):
        """Validate model fields before saving."""
        if self.title:
            self.title = self.title.strip()
        if self.description:
            self.description = self.description.strip()
