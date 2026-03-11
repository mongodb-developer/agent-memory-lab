"""
Seed script: generates 100 realistic Airbnb-style listings and inserts them
into voyage_lab.listings, mirroring the behaviour of seed.js.
"""
import os
import random
import datetime
from pymongo import MongoClient

MONGODB_URI = os.environ.get(
    'MONGODB_URI',
    'mongodb://admin:mongodb@localhost:27017/?directConnection=true'
)

cities = [
    {'city': 'London',        'country': 'United Kingdom', 'country_code': 'GB', 'market': 'London',        'coords': [-0.1278,    51.5074]},
    {'city': 'Paris',         'country': 'France',         'country_code': 'FR', 'market': 'Paris',         'coords': [2.3522,     48.8566]},
    {'city': 'Barcelona',     'country': 'Spain',          'country_code': 'ES', 'market': 'Barcelona',     'coords': [2.1734,     41.3851]},
    {'city': 'Amsterdam',     'country': 'Netherlands',    'country_code': 'NL', 'market': 'Amsterdam',     'coords': [4.9041,     52.3676]},
    {'city': 'Lisbon',        'country': 'Portugal',       'country_code': 'PT', 'market': 'Lisbon',        'coords': [-9.1393,    38.7223]},
    {'city': 'Porto',         'country': 'Portugal',       'country_code': 'PT', 'market': 'Porto',         'coords': [-8.6291,    41.1579]},
    {'city': 'Berlin',        'country': 'Germany',        'country_code': 'DE', 'market': 'Berlin',        'coords': [13.4050,    52.5200]},
    {'city': 'Rome',          'country': 'Italy',          'country_code': 'IT', 'market': 'Rome',          'coords': [12.4964,    41.9028]},
    {'city': 'New York',      'country': 'United States',  'country_code': 'US', 'market': 'New York',      'coords': [-73.9857,   40.7484]},
    {'city': 'Toronto',       'country': 'Canada',         'country_code': 'CA', 'market': 'Toronto',       'coords': [-79.3832,   43.6532]},
    {'city': 'Vancouver',     'country': 'Canada',         'country_code': 'CA', 'market': 'Vancouver',     'coords': [-123.1216,  49.2827]},
    {'city': 'Montreal',      'country': 'Canada',         'country_code': 'CA', 'market': 'Montreal',      'coords': [-73.5674,   45.5017]},
    {'city': 'Calgary',       'country': 'Canada',         'country_code': 'CA', 'market': 'Calgary',       'coords': [-114.0719,  51.0447]},
    {'city': 'Buenos Aires',  'country': 'Argentina',      'country_code': 'AR', 'market': 'Buenos Aires',  'coords': [-58.3816,  -34.6037]},
    {'city': 'São Paulo',     'country': 'Brazil',         'country_code': 'BR', 'market': 'São Paulo',     'coords': [-46.6333,  -23.5505]},
    {'city': 'Rio de Janeiro','country': 'Brazil',         'country_code': 'BR', 'market': 'Rio de Janeiro','coords': [-43.1729,  -22.9068]},
    {'city': 'Bogotá',        'country': 'Colombia',       'country_code': 'CO', 'market': 'Bogotá',        'coords': [-74.0721,    4.7110]},
    {'city': 'Medellín',      'country': 'Colombia',       'country_code': 'CO', 'market': 'Medellín',      'coords': [-75.5812,    6.2442]},
    {'city': 'Santiago',      'country': 'Chile',          'country_code': 'CL', 'market': 'Santiago',      'coords': [-70.6483,  -33.4569]},
    {'city': 'Lima',          'country': 'Peru',           'country_code': 'PE', 'market': 'Lima',          'coords': [-77.0428,  -12.0464]},
    {'city': 'Tokyo',         'country': 'Japan',          'country_code': 'JP', 'market': 'Tokyo',         'coords': [139.6917,   35.6895]},
    {'city': 'Sydney',        'country': 'Australia',      'country_code': 'AU', 'market': 'Sydney',        'coords': [151.2093,  -33.8688]},
]

property_types = ['Apartment', 'House', 'Loft', 'Condo', 'Villa', 'Studio', 'Townhouse', 'Cottage']
room_types     = ['Entire home/apt', 'Private room', 'Shared room']
cancellation   = ['flexible', 'moderate', 'strict', 'super_strict_30']

summaries = [
    'A stunning apartment in the heart of the city, steps from top restaurants and museums. Enjoy panoramic views and modern amenities in this beautifully renovated space.',
    'Charming historic home with original architectural details. High ceilings, exposed brick, and a sun-drenched living room make this the perfect urban retreat.',
    'Modern loft-style apartment with floor-to-ceiling windows. Fully equipped kitchen, fast WiFi, and a dedicated workspace ideal for digital nomads.',
    'Cozy boutique retreat in a quiet neighbourhood. Walking distance to parks, cafés, and public transport. Perfect for couples or solo travellers.',
    'Elegant and spacious villa with private garden. Professionally decorated with premium furnishings, offering a luxury stay in an unbeatable location.',
    'Minimalist studio with everything you need. Smart TV, Netflix, espresso machine, and blackout curtains for a restful stay.',
    'Quaint cottage with rustic charm and modern comforts. Fireplace, fully stocked kitchen, and a garden patio ideal for relaxing evenings.',
    'Contemporary condo on a high floor with city skyline views. Gym and pool access included. Business-friendly with concierge service.',
    'Sun-filled townhouse spread across three floors. Pet-friendly, with a private rooftop terrace and dedicated parking.',
    'Welcoming apartment in a lively cultural district. Local galleries, markets, and independent coffee shops right at your doorstep.',
    'Sleek waterfront condo with floor-to-ceiling glass and sweeping harbour views.',
    'Bright and airy suite in a heritage building, blending period architecture with contemporary interiors.',
    'Private garden apartment tucked away on a leafy residential street.',
    'Rooftop penthouse with 360-degree city views and a private terrace.',
    'Vibrant neighbourhood flat with colourful street art at every corner.',
    'Architect-designed open-plan home featuring bespoke furniture and curated original artwork.',
    'Tropical hideaway with lush jungle surroundings, a hammock on the veranda, and outdoor shower.',
    'Classic brownstone apartment on a tree-lined avenue, lovingly restored.',
    'Bright mountain-view suite with ski-in access in winter and hiking trails in summer.',
    'Bohemian artist studio with high raftered ceilings, skylights, and creative vibes.',
]

descriptions = [
    'The space is thoughtfully designed to balance comfort and style.',
    'Guests will have the entire place to themselves.',
    'A fully self-contained unit with private entrance.',
    'High-speed fibre WiFi throughout. Laptop-friendly desks in two rooms.',
    'The garden is maintained weekly and is perfect for morning coffee.',
    'Ample storage space, a full-size washing machine and dryer.',
    'The bedroom is separated from the living area by solid doors.',
    'Local artwork curated by the host adorns the walls.',
    'The building is serviced by a 24-hour concierge.',
    'Floor-to-ceiling bookshelves line the main wall.',
    'The kitchen is stocked with local spices and fresh coffee.',
    'Heated bathroom floors, rainfall shower, and a deep soaking tub.',
    'The terrace faces west for golden-hour sunsets.',
    'Soundproofed walls and blackout blinds ensure complete rest.',
    'Bike rentals are available through the host at a discount.',
    'The host has prepared a detailed digital guidebook.',
]

host_names = [
    'Alice', 'Marco', 'Sophie', 'David', 'Yuki', 'Elena', 'Carlos', 'Priya', 'Luca', 'Amara',
    'James', 'Mei', 'Valentina', 'Sebastián', 'Isabelle', 'Kwame', 'Natasha', 'Diego', 'Aiko',
    'Camille', 'Rafael', 'Nadia', 'Patrick', 'Lucía', 'Omar', 'Ingrid', 'Felipe', 'Zara', 'Hiroshi', 'Chloe',
]

host_abouts = [
    'I love welcoming guests from around the world and sharing local tips.',
    'Superhost for 5 years. I live nearby and am always happy to help.',
    'Travel enthusiast and interior designer.',
    'Local food blogger and tour guide.',
    'Architect by profession. This property is my passion project.',
    'Born and raised here, I know every shortcut and hidden gem.',
    'I work in hospitality and bring professional attention to detail.',
    'Passionate about sustainable travel.',
    'Artist and musician.',
    'I manage several properties but treat each guest as family.',
    'Retired teacher and lifelong host.',
    'Digital nomad for 10 years before settling here.',
]

amenity_pool = [
    'WiFi', 'Kitchen', 'TV', 'Washing machine', 'Air conditioning', 'Heating', 'Dedicated workspace',
    'Hair dryer', 'Iron', 'Hangers', 'Coffee maker', 'Microwave', 'Refrigerator', 'Dishwasher',
    'Essentials', 'Shampoo', 'Hot water', 'Bed linens', 'Extra pillows and blankets',
    'First aid kit', 'Fire extinguisher', 'Smoke alarm', 'Carbon monoxide alarm',
    'Long term stays allowed', 'Self check-in', 'Lock box', 'Luggage dropoff allowed',
    'Garden', 'Balcony', 'Patio', 'BBQ grill', 'Pool', 'Gym', 'Elevator', 'Parking',
    'Pets allowed', 'Children friendly', 'Crib', 'High chair',
]


def rand_int(lo, hi):
    return random.randint(lo, hi)


def rand_float(lo, hi, decimals=2):
    return round(random.uniform(lo, hi), decimals)


def rand_date(start_year=2015, end_year=2023):
    start = datetime.datetime(start_year, 1, 1)
    end   = datetime.datetime(end_year, 12, 31)
    delta = end - start
    return start + datetime.timedelta(days=random.randint(0, delta.days))


def make_listing(i):
    city_data    = random.choice(cities)
    prop_type    = random.choice(property_types)
    room_type    = random.choice(room_types)
    bedrooms     = rand_int(1, 5)
    beds         = bedrooms + rand_int(0, 2)
    bathrooms    = round(rand_int(1, bedrooms + 1) * 0.5 + 0.5, 1)
    price        = rand_int(40, 500)
    host_name    = random.choice(host_names)
    host_id      = rand_int(10000, 99999)
    lon, lat     = city_data['coords']
    amenities    = random.sample(amenity_pool, rand_int(6, 20))
    created_at   = rand_date()
    last_review  = rand_date(2022, 2024)

    return {
        'listing_url':            f'https://www.airbnb.com/rooms/{1000000 + i}',
        'name':                   f'{prop_type} in {city_data["city"]} #{i + 1}',
        'summary':                random.choice(summaries),
        'description':            random.choice(descriptions),
        'property_type':          prop_type,
        'room_type':              room_type,
        'bedrooms':               bedrooms,
        'beds':                   beds,
        'bathrooms':              bathrooms,
        'price':                  price,
        'weekly_price':           round(price * 6.5),
        'monthly_price':          round(price * 25),
        'minimum_nights':         rand_int(1, 7),
        'maximum_nights':         rand_int(30, 365),
        'availability_365':       rand_int(0, 365),
        'number_of_reviews':      rand_int(0, 300),
        'review_scores_rating':   rand_float(70, 100),
        'review_scores_accuracy': rand_float(8, 10),
        'review_scores_cleanliness': rand_float(8, 10),
        'review_scores_checkin':  rand_float(8, 10),
        'review_scores_communication': rand_float(8, 10),
        'review_scores_location': rand_float(8, 10),
        'review_scores_value':    rand_float(8, 10),
        'cancellation_policy':    random.choice(cancellation),
        'amenities':              amenities,
        'host': {
            'host_id':            str(host_id),
            'host_name':          host_name,
            'host_about':         random.choice(host_abouts),
            'host_is_superhost':  random.random() < 0.3,
            'host_listings_count': rand_int(1, 10),
            'host_since':         rand_date(2010, 2020),
        },
        'address': {
            'market':       city_data['market'],
            'city':         city_data['city'],
            'country':      city_data['country'],
            'country_code': city_data['country_code'],
        },
        'location': {
            'type':        'Point',
            'coordinates': [
                round(lon + rand_float(-0.05, 0.05, 4), 4),
                round(lat + rand_float(-0.05, 0.05, 4), 4),
            ],
        },
        'first_review':  created_at,
        'last_review':   last_review,
        'created_at':    created_at,
        'updated_at':    datetime.datetime.utcnow(),
    }


def main():
    print('Connecting to MongoDB...')
    client = MongoClient(MONGODB_URI, appName='devrel-workshop-agentmemory-seed')
    db     = client['voyage_lab']
    coll   = db['listings']

    existing = coll.count_documents({})
    if existing > 0:
        print(f'voyage_lab.listings already has {existing} documents — skipping seed.')
        client.close()
        return

    listings = [make_listing(i) for i in range(100)]
    result   = coll.insert_many(listings)
    print(f'Inserted {len(result.inserted_ids)} listings into voyage_lab.listings.')
    client.close()


if __name__ == '__main__':
    main()
