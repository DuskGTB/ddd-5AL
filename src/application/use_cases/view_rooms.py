from domain.model.room import Room

class ViewRooms:
    def execute(self) -> list[Room]:
        return Room.all_rooms()
