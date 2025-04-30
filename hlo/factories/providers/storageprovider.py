from faker.providers import BaseProvider, ElementsType

# https://github.com/joke2k/faker/blob/master/faker/providers/person/__init__.py

class StorageProvider(BaseProvider):
    room_locations: ElementsType[str] = ["{{room}} {{location}}"]
    buildings: ElementsType[str] = [
            "Warehouse",
            "Apartment",
            "Barn",
            ]
    rooms: ElementsType[str] = [
            "Kitchen",
            "Shed",
            "Bedroom",
            "Storage room",
            "Office",
            ]
    locations: ElementsType[str] = [
            "Closet",
            "Shelf",
            "Wardrobe",
            "Pantry",
            "Locker",
            "Dresser",
            "Counter",
            "Table",
            "Desk",
            ]
    containers: ElementsType[str] = [
            "Cardbord box",
            "Plastic box",
            "Binder",
            ]

    def room_location(self) -> str:
        pattern: str = self.random_element(self.room_locations)
        return self.generator.parse(pattern)

    def building(self) -> str:
        return self.random_element(self.buildings)

    def room(self) -> str:
        return self.random_element(self.rooms)

    def location(self) -> str:
        return self.random_element(self.locations)

    def container(self) -> str:
        return self.random_element(self.containers)
