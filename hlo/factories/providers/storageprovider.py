from faker.providers import BaseProvider, ElementsType

# https://github.com/joke2k/faker/blob/master/faker/providers/person/__init__.py


class StorageProvider(BaseProvider):
    room_locations: ElementsType[str] = ["{{room}} {{location}}"]
    three_items: ElementsType[str] = ["{{item}}, {{item}}, {{item}}"]

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
        "Grotto",
        "Hangar",
        "House",
        "Mansion",
        "Office",
        "Penthouse",
        "Residence",
        "Shed",
        "Shop",
        "Studio",
        "Temple",
        "Tepee",
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
        "Cabinet",
        "Chest",
        "Closet",
        "Counter",
        "Desk",
        "Dresser",
        "Drawer",
        "Locker",
        "Pantry",
        "Rack",
        "Shelf",
        "Stand",
        "Table",
        "Trunk",
        "Wardrobe",
    ]
    containers: ElementsType[str] = [
        "Bag",
        "Barrel",
        "Basket",
        "Binder",
        "Box",
        "Briefcase",
        "Cardboard box",
        "Crate",
        "Lunchbox",
        "Organizer bin",
        "Plastic box",
        "Storage bin",
        "Suitcase",
        "Toolbox",
    ]

    items: ElementsType[str] = [
        "Axe",
        "Backpack",
        "Ball",
        "Belt",
        "Binoculars",
        "Book",
        "Bow",
        "Camera",
        "Candle",
        "Canteen",
        "Compass",
        "Dagger",
        "Fishing rod",
        "Flashlight",
        "Flute",
        "Guitar",
        "Hammer",
        "Hatchet",
        "Hiking stick",
        "Knife",
        "Map",
        "Machete",
        "Maple syrup bottle",
        "Notebook",
        "Paddle",
        "Pickaxe",
        "Rope",
        "Saddlebag",
        "Saw",
    ]

    items_plural: ElementsType[str] = [
        "Axes",
        "Backpacks",
        "Balls",
        "Belts",
        "Binoculars",
        "Books",
        "Bows",
        "Cameras",
        "Candles",
        "Canteens",
        "Compasses",
        "Daggers",
        "Fishing rods",
        "Flashlights",
        "Flutes",
        "Guitars",
        "Hammers",
        "Hatchets",
        "Hiking sticks",
        "Knives",
        "Maps",
        "Machetes",
        "Maple syrup bottles",
        "Notebooks",
        "Paddles",
        "Pickaxes",
        "Ropes",
        "Saddlebags",
        "Saws",
    ]

    def multiple_items(
        self,
        count: int = -1,
        minimun: int = -1,
        maximum: int = -1,
    ) -> str:
        mitems = []
        if count == -1:
            count = self.generator.random_int(minimun, maximum)
        for _ in range(count):
            mitems.append(self.random_element(self.items_plural))  # noqa: PERF401
        return ", ".join(mitems).capitalize()

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

    def item(self) -> str:
        return self.random_element(self.items)
