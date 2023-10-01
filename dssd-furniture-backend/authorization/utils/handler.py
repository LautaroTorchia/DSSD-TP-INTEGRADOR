import datetime
from django.db.models import Q
from rest_framework_tracking.models import APIRequestLog
from authentication.models import User
from authorization.models import UserRole, PermissionRole

def get_historical_role_log():
    """Return historical roles."""    
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path__contains='/api/authorization/role')]
    return result

def get_historical_permission_role_log():
    """Return historical permission roles."""
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path__contains='api/authorization/permission-role')]
    return result

def get_historical_user_role_log():
    """Return historical user roles."""
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path__contains='api/authorization/user-role')]
    return result

def get_historical_view_descriptor_log():
    """Return historical view descriptors."""
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path__contains='api/authorization/view-descriptor')]
    return result

def get_historical_role_log_by_id(id):
    """Return historical roles by ID."""
    path = '/api/authorization/role/' + str(id) + '/'
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path=path)]
    return result

def get_historical_permission_role_log_by_id(id):
    """Return historical permission roles by ID."""
    path = '/api/authorization/permission-role/' + str(id) + '/' 
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path=path)]
    return result

def get_historical_user_role_log_by_id(id):
    """Return historical user roles by ID."""
    path = '/api/authorization/user-role/' + str(id) + '/' 
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path=path)]
    return result

def get_historical_view_descriptor_log_by_id(id):
    """Return historical view descriptors by ID."""
    path = '/api/authorization/view-descriptor/' + str(id) + '/'    
    result = [{"id": item.id, "requested_at": item.requested_at, "response_ms": item.response_ms, "user": item.user.email if isinstance(item.user, User) else "not_logged", "view_method": item.method, "status_code": item.status_code, "remote_addr": item.remote_addr, "host": item.host, "query_params": item.query_params, "path":item.path} for item in APIRequestLog.objects.filter(path=path)]
    return result

def get_user_role_by_date(user_email, start_date, end_date):
    """Return historical roles for user on delta date."""    
    start_date_year = start_date.split('-')[0]
    start_date_month = start_date.split('-')[1]
    start_date_day = start_date.split('-')[2]
    end_date_year = end_date.split('-')[0]
    end_date_month = end_date.split('-')[1]
    end_date_day = end_date.split('-')[2]
    
    result = [{"id": n.id, "creator": n.creator.email, "user":n.user_id.email, "role": n.role_id.denomination, "created_at": n.created_at} for n in UserRole.objects.filter(Q(user_id__email=user_email) & Q(created_at__date__gte=datetime.date(int(start_date_year),int(start_date_month),int(start_date_day))) & Q(created_at__date__lte=datetime.date(int(end_date_year),int(end_date_month),int(end_date_day))))]

    return result

def get_permission_role_by_date(role_id, start_date, end_date):
    """Return historical permission by roles on delta date."""    
    start_date_year = start_date.split('-')[0]
    start_date_month = start_date.split('-')[1]
    start_date_day = start_date.split('-')[2]
    end_date_year = end_date.split('-')[0]
    end_date_month = end_date.split('-')[1]
    end_date_day = end_date.split('-')[2]

    result = [{"id": n.id, "approver": n.owner.email, "permission":n.view_id.denomination, "role": n.role_id.denomination, "created_at": n.created_at} for n in PermissionRole.objects.filter(Q(role_id__id=role_id) & Q(created_at__date__gte=datetime.date(int(start_date_year),int(start_date_month),int(start_date_day))) & Q(created_at__date__lte=datetime.date(int(end_date_year),int(end_date_month),int(end_date_day))))]
    return result

def get_permission_user_by_date(email, start_date, end_date):
    """Return historical user permission by roles on delta date."""    
    start_date_year = start_date.split('-')[0]
    start_date_month = start_date.split('-')[1]
    start_date_day = start_date.split('-')[2]
    end_date_year = end_date.split('-')[0]
    end_date_month = end_date.split('-')[1]
    end_date_day = end_date.split('-')[2]

    result = []

    for iter_role in UserRole.objects.filter(Q(user_id__email=email) & Q(created_at__date__gte=datetime.date(int(start_date_year),int(start_date_month),int(start_date_day))) & Q(created_at__date__lte=datetime.date(int(end_date_year),int(end_date_month),int(end_date_day)))):
        for iter_permission in PermissionRole.objects.filter(Q(role_id__id=iter_role.role_id.id) & Q(created_at__date__gte=datetime.date(int(start_date_year),int(start_date_month),int(start_date_day))) & Q(created_at__date__lte=datetime.date(int(end_date_year),int(end_date_month),int(end_date_day)))):
            result.append({"role": iter_role.role_id.denomination, "iter_role_since": iter_role.created_at, "role_approver": iter_role.creator.email, "permitted_since": iter_permission.created_at, "permission_approver": iter_permission.owner.email, "permission":iter_permission.view_id.denomination})
    return result