from django.contrib import admin
from octopusdash.registry import dashboard
# Register your models here.


from .models import Project, Task, Milestone, ProjectMember, BudgetExpense

# Register each model with the custom dashboard (or django admin)
dashboard.register(Project)
dashboard.register(Task)
dashboard.register(Milestone)
dashboard.register(ProjectMember)
dashboard.register(BudgetExpense)
