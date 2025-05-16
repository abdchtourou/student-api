from typing import Any, Dict, List, Optional, Type, Union
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from django.db.models import QuerySet, Q, Count, Case, When, BooleanField, F
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.utils import timezone
from django.db.models import F
from .models import Todo
from .serializers import TodoSerializer
from .pagination import StandardResultsSetPagination
from student.models import Student


class IsOwner(permissions.BasePermission):
    
    def has_permission(self, request: Request, view: Any) -> bool:
      
        return True  # Initial permission granted, object level check follows

    def has_object_permission(self, request: Request, view: Any, obj: Todo) -> bool:
      
        return obj.student.user == request.user


class TodoViewSet(viewsets.ModelViewSet):
    
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'is_completed', 'title']
    ordering = ['-created_at']

    def get_queryset(self) -> QuerySet:
        """Get the queryset of todos for the current user.
        
        Returns:
            QuerySet of Todo objects owned by the current user
        """
        return Todo.objects.select_related('student__user').filter(
            student__user=self.request.user,
            is_deleted=False
        )

    def get_serializer_context(self) -> Dict[str, Any]:
        
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
       
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "todos": serializer.data
        })

    @action(detail=False, methods=['get'])
    def completed(self, request: Request) -> Response:
      
        completed_todos = self.get_queryset().filter(is_completed=True)
        serializer = self.get_serializer(completed_todos, many=True)
        return Response({
            "count": completed_todos.count(),
            "todos": serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def pending(self, request: Request) -> Response:
  
        pending_todos = self.get_queryset().filter(is_completed=False)
        serializer = self.get_serializer(pending_todos, many=True)
        return Response({
            "count": pending_todos.count(),
            "todos": serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request: Request) -> Response:
       
        ids = request.data.get('ids', [])
        if not ids:
            raise ValidationError({'ids': _('No todo IDs provided')})
            
        with transaction.atomic():
            deleted_count = self.get_queryset().filter(id__in=ids).update(is_deleted=True, deleted_at=timezone.now())[0]
            
        return Response({
            'message': _('Successfully deleted {count} todos').format(count=deleted_count),
            'deleted_count': deleted_count
        })

    @action(detail=False, methods=['post'])
    def bulk_toggle_complete(self, request: Request) -> Response:
        """Toggle completion status for multiple todos at once.
        
        Args:
            request: The incoming request with todo ids and target status
            
        Returns:
            Response indicating success and updated todos
        """
        ids = request.data.get('ids', [])
        target_status = request.data.get('is_completed', True)
        
        if not ids:
            raise ValidationError({'ids': _('No todo IDs provided')})
            
        with transaction.atomic():
            # Only update todos owned by the current user
            updated_todos = self.get_queryset().filter(id__in=ids)
            updated_count = updated_todos.update(
                is_completed=target_status,
                updated_at=timezone.now()
            )
            
            # Get the updated todos for response
            updated_todos = self.get_queryset().filter(id__in=ids)
            serializer = self.get_serializer(updated_todos, many=True)
            
            return Response({
                'message': _('Successfully updated {count} todos').format(count=updated_count),
                'updated_count': updated_count,
                'todos': serializer.data
            })

    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request: Request, pk=None) -> Response:
       
        todo = self.get_object()
        todo.is_completed = not todo.is_completed
        todo.save(update_fields=['is_completed', 'updated_at'])
        serializer = self.get_serializer(todo)
        return Response(serializer.data)

    def perform_create(self, serializer: ModelSerializer) -> None:
      
        try:
            student = Student.objects.select_related('user').get(user=self.request.user)
            serializer.save(student=student)
        except Student.DoesNotExist:
            raise PermissionDenied(_('You must be a registered student to create a task.'))

    def perform_update(self, serializer: ModelSerializer) -> None:
      
        serializer.save()

    def perform_destroy(self, instance: Todo) -> None:
        """Soft delete a todo instance.
        
        Args:
            instance: The todo instance to delete
        """
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save(update_fields=['is_deleted', 'deleted_at'])
