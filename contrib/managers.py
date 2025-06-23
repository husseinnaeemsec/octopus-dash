from django.db.models import Manager,Q
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class DashboardModelManager(Manager):
    
    ''' Custom manager for Octopusdash to dynamicly control the query set for registred models  '''
    def __init__(self, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model is not None:
            self.model = model

    

    def filter_by_fields(self, filter_data: dict | None = None,queryset=None):
        queryset = self.get_queryset()

        if queryset is None:
            queryset = self.get_queryset()


        if not filter_data:
            return queryset

        for field_name, filter_info in filter_data.items():
            field_type = filter_info.get('type')
            
            
            if 'date' in  field_type or field_type == 'time':
                
                start_str,_,end_str = filter_info.get("value").partition("&") if filter_info.get("value",None) is not None else None,None,None

                try:
                    if start_str and end_str:
                        start_date = datetime.strptime(start_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                        queryset = queryset.filter(**{f"{field_name}__range": (start_date, end_date)})

                    elif start_str:
                        start_date = datetime.strptime(start_str, "%Y-%m-%d")
                        queryset = queryset.filter(**{f"{field_name}__gte": start_date})
                    elif end_str:
                        end_date = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                        queryset = queryset.filter(**{f"{field_name}__lte": end_date})

                except Exception as e:
                    # Handle invalid date format gracefully
                    continue  # or log the error
            
            elif field_type == 'bool':
                value = filter_info['value']
                
                
                if value is not None:
                    query = {f"{field_name}":filter_info['value']}
                    queryset.filter(**query)

        return queryset



    def search(self, query, search_fields=None,queryset=None):
        """
        Perform a dynamic search on given fields using Q objects.

        :param query: The search string.
        :param search_fields: List of fields to search on (strings).
        :return: queryset filtered by OR-ing Q lookups on each field.
        """
        
        if queryset is None:
            queryset = self.get_queryset()
        
        if not query or not search_fields:
            return self.get_queryset()

        q_objects = Q()
        for field in search_fields:
            # Support __icontains lookups
            lookup = f"{field}__icontains"
            q_objects |= Q(**{lookup: query})

        return self.get_queryset().filter(q_objects)