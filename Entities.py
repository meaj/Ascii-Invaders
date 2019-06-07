"""
Ascii Invaders - GameVariables
 * A class containing the entity classes used by Ascii Invaders
 * Copyright (C) 2019 Meaj
"""


# A class which represents the projectile entities
class Entity:
    def __init__(self, active=False,  x_pos=-1, y_pos=-1, heading=0):
        self.active = active
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = heading

    def set_all_values(self, active=False, x_pos=-1, y_pos=-1, heading=0):
        self.active = active
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.heading = heading

    def set_coordinates(self, x_val, y_val):
        self.x_pos = x_val
        self.y_pos = y_val

    def set_x(self, x_val):
        self.x_pos = x_val

    def set_y(self, y_val):
        self.y_pos = y_val

    def set_heading(self, heading):
        self.heading = heading

    def get_heading(self):
        return self.heading

    def get_x(self):
        return self.x_pos

    def get_y(self):
        return self.y_pos

    def set_active(self, active):
        self.active = active

    def is_active(self):
        return self.active

    def disable(self):
        self.active = False
        self.x_pos = -1
        self.y_pos = -1
        self.heading = 0


# A class which represents the player and enemy entities, it inherits from the Entity class
class VehicleEntity(Entity):
    def __init__(self, active=False, x_pos=-1, y_pos=-1, firing=False, fire_order=-1, heading=0):
        super().__init__(active, x_pos, y_pos, heading)
        self.firing = firing
        self.fire_order = fire_order

    def set_all_values(self, active=False, x_pos=-1, y_pos=-1, firing=False, fire_order=-1, heading=0):
        super().set_all_values(active, x_pos, y_pos, heading)
        self.firing = firing
        self.fire_order = fire_order

    def set_fire_order(self, fire_order):
        self.fire_order = fire_order

    def get_fire_order(self):
        return self.fire_order

    def get_coordinates_array(self):
        coordinates = [self.x_pos, self.y_pos]
        return coordinates

    def shift_down(self):
        self.x_pos += 1

    def toggle_fired(self):
        self.firing = not self.firing

    def reload(self):
        self.firing = False

    def disable(self):
        super().disable()
        self.firing = False
        self.fire_order = -1
