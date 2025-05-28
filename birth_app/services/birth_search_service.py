from ..models import BirthRegistrationApplication

class BirthRegistrationSearchService:
    def search_birth_registrations(self, tenant_id=None, statuses=None, ids=None, app_num=None):
        """
        Search birth registration applications with filters
        
        Args:
            tenant_id (str): Filter by tenant ID
            statuses (list): Filter by list of statuses
            ids (list): Filter by list of application IDs
            app_num (str): Filter by application number
            
        Returns:
            QuerySet: Filtered birth registration applications
        """
        # Start with base queryset
        qs = BirthRegistrationApplication.objects.all()
        
        # Apply filters only if parameters are provided and valid
        if tenant_id and isinstance(tenant_id, str):
            qs = qs.filter(tenant_id=tenant_id)
            
        if statuses and isinstance(statuses, list):
            qs = qs.filter(status__in=statuses)
            
        if ids and isinstance(ids, list):
            # Convert string IDs to integers if needed
            try:
                ids = [int(id) for id in ids]
                qs = qs.filter(id__in=ids)
            except (ValueError, TypeError):
                # If IDs can't be converted to integers, return empty queryset
                return BirthRegistrationApplication.objects.none()
                
        if app_num and isinstance(app_num, str):
            qs = qs.filter(application_number=app_num)
            
        # Return ordered results
        
        return qs.order_by('id')