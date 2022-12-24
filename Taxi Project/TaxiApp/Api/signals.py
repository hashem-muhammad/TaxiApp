from django.db.models.signals import post_save
from Api.models import Trip
from Api.FCM_Manager import send_notify
from django.dispatch import receiver


@receiver(post_save, sender=Trip)
def send_notify(sender, instance, created, *args, **kwargs):
    if created or not created:
        user_toke = instance.user.firebase_token
        driver_token = instance.driver.firebase_token
        trip_id = instance.id
        status = instance.status
        try:
            if status.lower() == 'new':
                send_notify(driver_token, 'new order', trip_id)
            else:
                send_notify(user_toke, 'new order status', trip_id)
            
        except:
            pass
    else:
        user_toke = instance.user.firebase_token
        driver_token = instance.driver.firebase_token
        trip_id = instance.id
        status = instance.status
        try:
            if status.lower() == 'new':
                send_notify(driver_token, 'new order', trip_id)
            else:
                send_notify(user_toke, 'new order status', trip_id)
            
        except:
            pass