from .base import db
from .role import Role
from .user import User
from .points_of_sale import Points_of_sale
from .driver_status import Driver_status
from .driver import Driver
from .vehicle_type import Vehicle_type
from .vehicle import Vehicle
from .load_type import Load_type
from .orders_status import Orders_status
from .orders import Orders

__all__ = ['db', 'Role', 'User', 'Points_of_sale', 'Driver_status', 'Driver', 'Vehicle_type', 'Vehicle', 'Load_type', 'Orders_status', 'Orders']

from src.models import *