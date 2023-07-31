from tortoise import Tortoise, run_async
from tortoise.queryset import AwaitableQuery

from modules import Hotel, Room, Client


async def create_database():
    await Tortoise.init(
        db_url=f"sqlite://Services.sqlite3",
        modules={"modules": ["modules"]}
    )
    await Tortoise.generate_schemas()


async def insert_data():
    hotel_1 = Hotel(name="Hotel A", description="Luxury hotel",
                    stars=5, minimal_price=1000)
    await hotel_1.save()

    hotel_2 = Hotel(name="Hotel B", description="Budget hotel",
                    stars=3, minimal_price=100)
    await hotel_2.save()

    room_1 = Room(hotel=hotel_1, count_of_person=1, price=1000)
    await room_1.save()

    room_2 = Room(hotel=hotel_1, count_of_person=1, price=5000)
    await room_2.save()

    room_3 = Room(hotel=hotel_1, count_of_person=2, price=3000)
    await room_3.save()

    room_4 = Room(hotel=hotel_2, count_of_person=1, price=100)
    await room_4.save()

    room_5 = Room(hotel=hotel_2, count_of_person=1, price=200)
    await room_5.save()

    room_6 = Room(hotel=hotel_2, count_of_person=2, price=250)
    await room_6.save()

    client_1 = Client(room=room_1, full_name="John Doe", phone_number="123456789",
                      date_start="2023-08-01", date_end="2023-08-05")
    await client_1.save()

    client_2 = Client(room=room_2, full_name="Jane Smith",
                      phone_number="987654321", date_start="2023-08-02", date_end="2023-08-04")
    await client_2.save()

    client_3 = Client(room=room_3, full_name="Kane Bem",
                      phone_number="987654120", date_start="2023-08-02", date_end="2023-08-04")
    await client_3.save()

    client_4 = Client(room=room_3, full_name="Kane Bem",
                      phone_number="988951120", date_start="2023-08-02", date_end="2023-08-04")
    await client_4.save()

    client_5 = Client(room=room_4, full_name="Kol Ytkin",
                      phone_number="988951120", date_start="2023-08-02", date_end="2023-08-04")
    await client_5.save()

    client_6 = Client(room=room_5, full_name="kane Smirnov",
                      phone_number="988951120", date_start="2023-08-02", date_end="2023-08-04")
    await client_6.save()

    client_7 = Client(room=room_6, full_name="Dol Ytkin",
                      phone_number="988951120", date_start="2023-08-02", date_end="2023-08-04")
    await client_7.save()
    client_8 = Client(room=room_6, full_name="Nok Ytkin",
                      phone_number="988951120", date_start="2023-08-02", date_end="2023-08-04")
    await client_8.save()


async def get_cheapest_room():
    cheapest_room = await Hotel.all().order_by("minimal_price").first().values()
    print(
        f"The cheapest room located in hotel {cheapest_room['name']} and price is {cheapest_room['minimal_price']}")


async def sort_hotels_by_minimal_price():
    hotels = await Hotel.all().order_by("minimal_price").values()
    print("\nSorted by minimal_price")
    for hotel in hotels:
        print(hotel['name'])


async def list_of_clients_by_room_price():
    clients = await Client.all().prefetch_related("room__hotel").order_by("room__price")
    print("List of client sorted by room price")
    for client in clients:
        print(f"{client.full_name} {client.room.hotel.name} - {client.room.price}")


async def get_first_client():
    hotels = await Hotel.all()
    print("\nFirst client for each hotel:")
    for hotel in hotels:
        first_client = await Client.filter(room__hotel=hotel).order_by("date_start").first()
        print(
            f"For hotel {hotel.name} first client is {first_client.full_name}")


async def get_phone_expensive_phone_number():
    hotels = await Hotel.all()
    print("The person, who use most expensive room: ")
    for hotel in hotels:
        client = await Client.filter(room__hotel=hotel).order_by("-room__price")
        print(f"{client[0].phone_number}")


async def main():
    await create_database()
    await insert_data()
    await get_cheapest_room()
    await sort_hotels_by_minimal_price()
    await list_of_clients_by_room_price()
    await get_first_client()
    await get_phone_expensive_phone_number()


if __name__ == "__main__":
    run_async(main())
