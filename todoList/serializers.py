from typing import Dict, Any
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Todo
from student.serializers import StudentSerializer


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model.
    
    Handles serialization and deserialization of Todo instances,
    including nested representation of the associated student.
    """
    # Nested serializers
    student = StudentSerializer(read_only=True)
    
    # Extra fields
    status = serializers.SerializerMethodField()
    time_since_creation = serializers.SerializerMethodField()
    
    class Meta:
        """Meta class for TodoSerializer."""
        model = Todo
        fields = [
            'id', 'title', 'description', 'is_completed', 
            'created_at', 'updated_at', 'student', 'status',
            'time_since_creation'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_status(self, obj: Todo) -> str:
        """Get the status of the todo in a human-readable format.
        
        Args:
            obj: The Todo instance
            
        Returns:
            A string representing the status: 'Completed' or 'Pending'
        """
        return _('Completed') if obj.is_completed else _('Pending')
    
    def get_time_since_creation(self, obj: Todo) -> str:
        """Calculate how much time has passed since the todo was created.
        
        Args:
            obj: The Todo instance
            
        Returns:
            A string representing the time elapsed since creation
        """
        from django.utils import timezone
        from django.utils.timesince import timesince
        return timesince(obj.created_at, timezone.now())

    def validate_title(self, value: str) -> str:
        """Validate the title field.
        
        Args:
            value: The title value to validate
            
        Returns:
            The validated title
            
        Raises:
            ValidationError: If title is empty or just whitespace
        """
        if not value.strip():
            raise serializers.ValidationError(_('Title cannot be empty or just whitespace.'))
        return value.strip()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Perform object-level validation on the entire set of attributes.
        
        Args:
            attrs: Dictionary of attributes to validate
            
        Returns:
            The validated attributes dictionary
        """
        # Strip whitespace from text fields
        if 'description' in attrs and attrs['description']:
            attrs['description'] = attrs['description'].strip()
        return attrs
    
    def to_representation(self, instance: Todo) -> Dict[str, Any]:
        """Customize the output representation of a Todo instance.
        
        Args:
            instance: The Todo instance being serialized
            
        Returns:
            Dictionary representation of the Todo instance
        """
        representation = super().to_representation(instance)
        # Add custom formatting or conditional fields here if needed
        return representation
