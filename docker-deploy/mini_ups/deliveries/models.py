from django.contrib.auth.models import User
from django.db import models

# Create your models here.

TRUCK_STATUS = (
    ('idle', 'IDLE'),
    ('travelling', 'TRAVELLING'),
    ('loading', 'LOADING'),
    ('delivering', 'DELIVERING')
)

PACKAGE_STATUS = (
    ('waiting to be picked up', 'WAITING'),
    ('out for delivery', 'OUT'),
    ('delivered', 'DELIVERED')
)

class UPSAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acct_number = models.IntegerField()
    world_id = models.IntegerField()


    def __str__(self):
        return f"<UPSAccount :: user - {self.user.username} " \
               f"| acct_number - {self.acct_number} " \
               f"| world_id - {self.world_id} >"


class Truck(models.Model):
    truck_id = models.AutoField(primary_key=True)
    world_id = models.IntegerField()
    status = models.CharField(max_length=50, choices=TRUCK_STATUS)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()

    def __str__(self):
        return f"<Truck :: truck_id - {self.truck_id} " \
               f"| world_id - {self.world_id} " \
               f"| status - {self.status}" \
               f"| position - ({self.pos_x}, {self.pos_y}) >"


class Package(models.Model):
    package_id = models.IntegerField(primary_key=True) # we will treat package_id the same as tracking_number
    world_id = models.IntegerField()
    truck = models.ForeignKey(Truck, null=True, on_delete=models.CASCADE)
    ups_account = models.ForeignKey(UPSAccount, blank=True, null=True, on_delete=models.CASCADE)
    destination_pos_x = models.IntegerField()
    destination_pos_y = models.IntegerField()
    warehouse_id = models.IntegerField()
    warehouse_pos_x = models.IntegerField()
    warehouse_pos_y = models.IntegerField()
    status = models.CharField(max_length=50, choices=PACKAGE_STATUS)
    # potentially include timestamps for "ready", "out for delivery", and "delivered"
    def __str__(self):
        return f"<Package :: package_id - {self.package_id} " \
               f"| world_id - {self.world_id} " \
               f"| ups_account - {self.ups_account.user.username} " \
               f"| destination - ({self.destination_pos_x}, {self.destination_pos_y}) " \
               f"| warehouse_id - {self.warehouse_id}" \
               f"| warehouse_loc - ({self.warehouse_pos_x}, {self.warehouse_pos_y}) " \
               f"| status - {self.status} >"


