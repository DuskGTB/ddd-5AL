from application.use_cases.view_rooms import ViewRooms

def test_view_rooms():
    uc = ViewRooms()
    rooms = uc.execute()
    assert isinstance(rooms, list)
    assert len(rooms) > 0
