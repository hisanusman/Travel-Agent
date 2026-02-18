"""
Script to populate Pinecone with travel destination data
"""

import json
import asyncio
from typing import List, Dict
from backend.rag.embeddings import embedding_generator
from backend.rag.retrieval import travel_retriever
from loguru import logger

# Comprehensive travel data for popular destinations
TRAVEL_DATA = [
    # MALDIVES
    {
        "destination": "Maldives",
        "category": "accommodation",
        "name": "Paradise Island Resort & Spa",
        "type": "Resort",
        "price_range": "$200-400/night",
        "rating": 4.5,
        "description": "Luxury overwater villas with private pools, spa, multiple restaurants, diving center. Perfect for honeymoons and luxury travelers.",
        "amenities": ["Private pool", "Spa", "Diving", "Water sports", "Fine dining"],
        "location": "North Male Atoll"
    },
    {
        "destination": "Maldives",
        "category": "accommodation",
        "name": "Maafushi Inn",
        "type": "Guesthouse",
        "price_range": "$50-100/night",
        "rating": 4.2,
        "description": "Budget-friendly guesthouse on local island. Clean rooms, local experience, easy access to excursions.",
        "amenities": ["Air conditioning", "WiFi", "Breakfast", "Tour desk"],
        "location": "Maafushi Island"
    },
    {
        "destination": "Maldives",
        "category": "accommodation",
        "name": "Soneva Fushi",
        "type": "Luxury Resort",
        "price_range": "$800-2000/night",
        "rating": 5.0,
        "description": "Ultra-luxury eco-resort with barefoot luxury concept. Private villas, outdoor cinema, observatory.",
        "amenities": ["Private beach", "Observatory", "Cinema", "Spa", "Diving", "Kids club"],
        "location": "Baa Atoll"
    },
    {
        "destination": "Maldives",
        "category": "activity",
        "name": "Snorkeling at Banana Reef",
        "type": "Water Activity",
        "price_range": "$40-60",
        "duration": "3-4 hours",
        "description": "Explore one of Maldives' most famous dive sites. See vibrant coral, sea turtles, reef sharks, and tropical fish.",
        "best_time": "Year-round",
        "difficulty": "Beginner-friendly"
    },
    {
        "destination": "Maldives",
        "category": "activity",
        "name": "Sunset Dolphin Cruise",
        "type": "Boat Tour",
        "price_range": "$35-50",
        "duration": "2-3 hours",
        "description": "Watch spinner dolphins at sunset while cruising the Indian Ocean. Includes refreshments.",
        "best_time": "Evening",
        "difficulty": "Easy"
    },
    {
        "destination": "Maldives",
        "category": "activity",
        "name": "Scuba Diving Certification",
        "type": "Water Activity",
        "price_range": "$400-600",
        "duration": "3-4 days",
        "description": "Get PADI Open Water certification in crystal clear waters. Includes all equipment and instruction.",
        "best_time": "Year-round",
        "difficulty": "All levels"
    },
    {
        "destination": "Maldives",
        "category": "dining",
        "name": "The Sea House Restaurant",
        "type": "Seafood Restaurant",
        "price_range": "$20-40",
        "cuisine": "Maldivian, Seafood",
        "description": "Fresh catch of the day, traditional Maldivian curry, beachfront dining.",
        "specialties": ["Grilled fish", "Mas huni", "Garudhiya soup"],
        "location": "Male"
    },
    {
        "destination": "Maldives",
        "category": "dining",
        "name": "Ithaa Undersea Restaurant",
        "type": "Fine Dining",
        "price_range": "$200-400",
        "cuisine": "European, Maldivian Fusion",
        "description": "World's first all-glass undersea restaurant. 180-degree panoramic views of marine life.",
        "specialties": ["Lobster medallion", "Yellowfin tuna", "Caviar"],
        "location": "Conrad Maldives"
    },
    
    # JAPAN - TOKYO
    {
        "destination": "Tokyo",
        "category": "accommodation",
        "name": "Park Hyatt Tokyo",
        "type": "Luxury Hotel",
        "price_range": "$400-800/night",
        "rating": 4.8,
        "description": "Iconic luxury hotel in Shinjuku. Featured in 'Lost in Translation'. Stunning city views, exceptional service.",
        "amenities": ["Pool", "Spa", "Fitness center", "Multiple restaurants", "City views"],
        "location": "Shinjuku"
    },
    {
        "destination": "Tokyo",
        "category": "accommodation",
        "name": "Capsule Hotel Anshin Oyado",
        "type": "Capsule Hotel",
        "price_range": "$30-50/night",
        "rating": 4.0,
        "description": "Modern capsule hotel experience. Clean, safe, great for budget travelers.",
        "amenities": ["WiFi", "Shared bathroom", "Lockers", "Common area"],
        "location": "Shibuya"
    },
    {
        "destination": "Tokyo",
        "category": "activity",
        "name": "Senso-ji Temple Visit",
        "type": "Cultural",
        "price_range": "Free",
        "duration": "2-3 hours",
        "description": "Tokyo's oldest temple in Asakusa. Explore Nakamise shopping street, beautiful architecture.",
        "best_time": "Morning (less crowded)",
        "difficulty": "Easy"
    },
    {
        "destination": "Tokyo",
        "category": "activity",
        "name": "Shibuya Crossing & Shopping",
        "type": "Shopping/Sightseeing",
        "price_range": "$0-100",
        "duration": "3-4 hours",
        "description": "Experience world's busiest intersection. Shop in Shibuya 109, visit Hachiko statue.",
        "best_time": "Afternoon/Evening",
        "difficulty": "Easy"
    },
    {
        "destination": "Tokyo",
        "category": "dining",
        "name": "Sukiyabashi Jiro",
        "type": "Sushi Restaurant",
        "price_range": "$300-500",
        "cuisine": "Japanese Sushi",
        "description": "3-Michelin star sushi restaurant. Featured in 'Jiro Dreams of Sushi'. Reservation required months in advance.",
        "specialties": ["Omakase", "Nigiri sushi"],
        "location": "Ginza"
    },
    {
        "destination": "Tokyo",
        "category": "dining",
        "name": "Ichiran Ramen",
        "type": "Ramen Shop",
        "price_range": "$8-15",
        "cuisine": "Japanese Ramen",
        "description": "Famous tonkotsu ramen chain. Individual booth dining for focused eating experience.",
        "specialties": ["Tonkotsu ramen", "Extra noodles"],
        "location": "Multiple locations"
    },
    
    # PARIS
    {
        "destination": "Paris",
        "category": "accommodation",
        "name": "Hotel Lutetia",
        "type": "Luxury Hotel",
        "price_range": "$500-1000/night",
        "rating": 4.9,
        "description": "Iconic Art Deco hotel in Saint-Germain. Legendary luxury, Michelin-star restaurant.",
        "amenities": ["Spa", "Pool", "Michelin restaurant", "Bar", "Concierge"],
        "location": "Saint-Germain-des-Prés"
    },
    {
        "destination": "Paris",
        "category": "accommodation",
        "name": "Generator Paris",
        "type": "Hostel",
        "price_range": "$30-80/night",
        "rating": 4.1,
        "description": "Trendy hostel with private and shared rooms. Rooftop bar, social atmosphere.",
        "amenities": ["Bar", "Cafe", "WiFi", "Common areas"],
        "location": "10th Arrondissement"
    },
    {
        "destination": "Paris",
        "category": "activity",
        "name": "Eiffel Tower Visit & Seine Cruise",
        "type": "Sightseeing",
        "price_range": "$50-80",
        "duration": "4-5 hours",
        "description": "Skip-the-line Eiffel Tower tickets plus 1-hour Seine river cruise. See Paris from two perspectives.",
        "best_time": "Sunset",
        "difficulty": "Easy"
    },
    {
        "destination": "Paris",
        "category": "activity",
        "name": "Louvre Museum Tour",
        "type": "Cultural",
        "price_range": "$20-60",
        "duration": "3-4 hours",
        "description": "World's largest art museum. See Mona Lisa, Venus de Milo, Egyptian antiquities.",
        "best_time": "Wednesday/Friday evenings (open late)",
        "difficulty": "Easy"
    },
    {
        "destination": "Paris",
        "category": "dining",
        "name": "Le Jules Verne",
        "type": "Fine Dining",
        "price_range": "$150-300",
        "cuisine": "French Haute Cuisine",
        "description": "Michelin-star restaurant in Eiffel Tower. Stunning views, exceptional cuisine by Frédéric Anton.",
        "specialties": ["Foie gras", "Dover sole", "Soufflé"],
        "location": "Eiffel Tower, 2nd Floor"
    },
    {
        "destination": "Paris",
        "category": "dining",
        "name": "L'As du Fallafel",
        "type": "Street Food",
        "price_range": "$8-15",
        "cuisine": "Middle Eastern",
        "description": "Best falafel in Paris. Always a queue but worth it. Marais district.",
        "specialties": ["Falafel sandwich", "Shawarma"],
        "location": "Le Marais"
    },
    
    # Add more destinations...
]

async def populate_database():
    """Populate Pinecone with travel data"""
    logger.info("Starting database population...")
    
    for idx, item in enumerate(TRAVEL_DATA):
        try:
            # Create searchable text
            text = f"""
            Destination: {item['destination']}
            Category: {item['category']}
            Name: {item['name']}
            Type: {item.get('type', '')}
            Price: {item.get('price_range', '')}
            Description: {item['description']}
            """
            
            if 'amenities' in item:
                text += f"\nAmenities: {', '.join(item['amenities'])}"
            if 'cuisine' in item:
                text += f"\nCuisine: {item['cuisine']}"
            if 'specialties' in item:
                text += f"\nSpecialties: {', '.join(item['specialties'])}"
            
            # Generate embedding
            embedding = embedding_generator.generate_embedding(text)
            
            # Store in Pinecone
            travel_retriever.index.upsert(
                vectors=[(
                    f"{item['destination']}_{item['category']}_{idx}",
                    embedding,
                    item  # Store full item as metadata
                )]
            )
            
            logger.info(f"Added: {item['destination']} - {item['name']}")
            
        except Exception as e:
            logger.error(f"Error adding {item.get('name', 'unknown')}: {e}")
    
    logger.info(f"✅ Successfully populated database with {len(TRAVEL_DATA)} items!")
    
    # Verify
    stats = travel_retriever.index.describe_index_stats()
    logger.info(f"Index stats: {stats}")

if __name__ == "__main__":
    asyncio.run(populate_database())
