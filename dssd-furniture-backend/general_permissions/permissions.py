from rest_framework import permissions
from django.db import connection
from resources.models import Resource

class IsPermittedRBAC(permissions.BasePermission):

	def has_permission(self, request, view):
		try:
			user = request.user
			view_descriptor = '.'.join((view.__module__, view.get_view_name()))     
			print(view_descriptor)
			permission_query = Resource.objects.filter(name='PERMISSION_QUERY')
			if len(permission_query) != 1:
				raise TypeError("Please review role-based access management query (PERMISSION_QUERY). hola")
			cursor = connection.cursor()        	
			cursor.execute(permission_query[0].content.format(user.id, view_descriptor))
			permissions_nro = cursor.fetchone()[0]
			return True if isinstance(permissions_nro, int) and permissions_nro > 0 else False
		except Exception as ex:
			from progralog.utils import generic_progra_log_error
			message = generic_progra_log_error()
			return False