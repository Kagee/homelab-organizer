from faker.providers import BaseProvider, ElementsType

# https://github.com/joke2k/faker/blob/master/faker/providers/person/__init__.py


class StorageProvider(BaseProvider):
    room_locations: ElementsType[str] = ["{{room}} {{location}}"]
    buildings: ElementsType[str] = [
        "Apartment",
        "Barn",
        "Bungalow",
        "Cabin",
        "Castle",
        "Condo",
        "Cottage",
        "Dormitory",
        "Flat",
        "Garage",
        "Hangar",
        "House",
        "Mansion",
        "Office",
        "Penthouse",
        "Residence",
        "Shed",
        "Shop",
        "Studio",
        "Townhouse",
        "Villa",
        "Warehouse",
        "Workshop",
        "Yard",
        "Ziggurat",
    ]
    rooms: ElementsType[str] = [
        "Atrium",
        "Attic",
        "Basement",
        "Bathroom",
        "Bedroom",
        "Breezeway",
        "CaveFamily room",
        "Cellar",
        "Closet",
        "Crawl space",
        "Craft room",
        "Dining room",
        "Den",
        "Exercise room",
        "Foyer",
        "Game room",
        "Garage",
        "Guest room",
        "Hall",
        "Home theater",
        "Kitchen",
        "Laundry room",
        "Library",
        "Living room",
        "Office",
        "Pantry",
        "Playroom",
        "Rec room",
        "Shed",
        "Storage area",
        "Storage room",
        "Study",
        "Utility room",
        "Workshop",
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
