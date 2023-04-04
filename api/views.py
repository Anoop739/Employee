from rest_framework.viewsets import  ModelViewSet
from rest_framework import   status
from rest_framework.response import Response
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        #  employee is eligible for promotion
        instance = self.get_object()
        experience = (date.today() - instance.date_of_joining).days / 365
        if not instance.manager and experience >= 5:
            instance.manager = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(data='Employee is not eligible for promotion')

    def partial_update(self, request, *args, **kwargs):
        # Check if the employee is being assigned to a department
        if 'department' in request.data:
            department_id = request.data['department']
            try:
                department = Department.objects.get(pk=department_id)
            except Department.DoesNotExist:
                return Response(data= 'Department does not exist')
            instance = self.get_object()
            instance.department = department
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return super().partial_update(request, *args, **kwargs)
