import json

class MovementExtractor:
    def get_movement(movement_name):
        movements = MovementExtractor.read_movements('movements.json')

        movement = None
        for each_movement in movements:
            if each_movement["name"] == movement_name:
                movement = each_movement
                break

        if movement == None:
            raise ValueError("Movement '%s' not found in movements.json" % (movement_name))

        return movement

    def read_movements(path):
        f = open(path)
        movements = json.load(f)
        return movements