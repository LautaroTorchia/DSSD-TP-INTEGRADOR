from .models import Progralog
from resources.models import ConfigMessage

def generic_progra_log_error():
    import sys, traceback
    exc_info = sys.exc_info()
    frame_info = exc_info[2].tb_frame
    detail_tb = traceback.format_exc()
    Progralog.objects.create(event_type="ERROR", frame_info=frame_info, tb_detail=detail_tb)
    for messages in ConfigMessage.objects.all():
    	if detail_tb.find(messages.content) != -1:
    		return messages.description
    return "Generic error. Please check log error!!!!."