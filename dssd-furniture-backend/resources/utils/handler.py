from django.db.models import Max
from resources.models import ConfigResource


def getActionToDeploy():
    """Return message on max ID on ConfigResource."""
    list_message = ConfigResource.objects.filter(is_archived=False).order_by('-id')
    if len(list_message) > 0:
    	message = list_message[0]
    	for config_item in list_message:
    		config_item.is_archived = True
    		config_item.save()
    	return message.content.content
    else:
    	return "No Action"