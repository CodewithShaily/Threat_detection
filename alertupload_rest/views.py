from alertupload_rest.serializers import UploadAlertSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
#from django.http import HttpResponse
#from storages.backends.s3boto3 import S3Boto3Storage
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework import status  # Import the status codes
from twilio.rest import Client
from threading import Thread
import re
from django.conf import settings
from django.http import JsonResponse


# Thread decorator definition
def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

# Upload alert

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def post_alert(request):
    serializer = UploadAlertSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        identify_email_sms(serializer)

    else:
        return JsonResponse({'error': 'Unable to process data!'}, status=400)

    return Response(request.META.get('HTTP_AUTHORIZATION'))


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t= Thread(target = function, args=args, kwargs=kwargs)
        t.daemon= True
        t.start()
    return decorator



# Identifies if the user provided an email or a mobile number
def identify_email_sms(serializer):

    if(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', serializer.data['alert_receiver'])):  
        print("Valid Email")
        send_email(serializer)
    elif re.compile("[+91][0-9]{10}").match(serializer.data['alert_receiver']):
        # 1) Begins with +3706
        # 2) Then contains 7 digits 
        print("Valid Mobile Number")
        send_sms(serializer)
    else:
        print("Invalid Email or Mobile number")

# Sends SMS
@start_new_thread
def send_sms(serializer):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(body=prepare_alert_message(serializer),
                                    from_=settings.TWILIO_NUMBER,
                                    to=serializer.data['alert_receiver'])

# Sends email
@start_new_thread
def send_email(serializer):
    send_mail('Threat Detected!', 
    prepare_alert_message(serializer), 
    'nagarrakshakk@gmail.com',
    [serializer.data['alert_receiver']],
    fail_silently=False,)

# Prepares the alert message
def prepare_alert_message(serializer):
    #image_data= split(serializer.data['image'],".")
    #uuid= image_data[0]
    uuid_with_slashes = split(serializer.data['image'], ".")
    uuid = split(uuid_with_slashes[3], "/")

    url = 'https://threat-detection-3.onrender.com/alert/' + uuid[2]

    return 'Threat Detected! View alert at ' + url

# Splits string into a list
def split(value, key):
    return str(value).split(key)
