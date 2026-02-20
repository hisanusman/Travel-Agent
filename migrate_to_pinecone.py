"""
Migrate all travel data to Pinecone using LOCAL embeddings (no API calls)
Uses sentence-transformers for embeddings - completely free and offline
"""

import json
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from loguru import logger
import time
import sys

# Configuration
PINECONE_API_KEY = "pcsk_7QaCsx_7LM1UqYuZ27tGM8SHCYMeLL4jBy2WptKkXBmZKBnSYHK8MsNm58gCUQQcxMiUm4"
INDEX_NAME = "travel-agent"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, efficient, 384 dimensions
DIMENSION = 384

print("🚀 Initializing migration to Pinecone...")
print(f"📦 Loading embedding model: {EMBEDDING_MODEL}")

# Initialize
pc = Pinecone(api_key=PINECONE_API_KEY)
model = SentenceTransformer(EMBEDDING_MODEL)

print("✅ Model loaded successfully!")

def create_index():
    """Create or recreate Pinecone index"""
    print(f"\n🔧 Setting up Pinecone index: {INDEX_NAME}")
    
    # Delete if exists
    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME in existing:
        print(f"🗑️  Deleting existing index...")
        pc.delete_index(INDEX_NAME)
        time.sleep(2)
    
    # Create new
    print(f"🆕 Creating new index with dimension {DIMENSION}...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    
    # Wait for ready
    while not pc.describe_index(INDEX_NAME).status['ready']:
        print("⏳ Waiting for index to be ready...")
        time.sleep(2)
    
    print("✅ Index ready!")
    return pc.Index(INDEX_NAME)

def create_text(item_type, item, city):
    """Create searchable text"""
    if item_type == "hotel":
        return f"{item['name']} is a {item.get('category', 'hotel')} in {city}. Price: {item.get('price_per_night', 'TBD')}/night. Rating: {item.get('rating', 'N/A')}. {item.get('description', '')} Amenities: {', '.join(item.get('amenities', []))}."
    elif item_type == "activity":
        return f"{item['name']} in {city}. {item.get('description', '')} Entry: {item.get('entry_fee', 'Free')}. Hours: {item.get('opening_hours', 'Varies')}. Best time: {item.get('best_time', 'Anytime')}."
    elif item_type == "restaurant":
        return f"{item['name']} restaurant in {city}. Cuisine: {item.get('cuisine', 'Local')}. Price: {item.get('price_range', 'Moderate')}. Rating: {item.get('rating', 'N/A')}. Specialties: {', '.join(item.get('specialties', []))}."
    return ""

def migrate():
    """Main migration function"""
    # Load data
    json_path = Path("data/travel_database.json")
    if not json_path.exists():
        print(f"❌ ERROR: {json_path} not found!")
        return
    
    with open(json_path) as f:
        data = json.load(f)
    
    print(f"\n📊 Loaded {len(data)} cities")
    
    # Create index
    index = create_index()
    
    # Process data
    vectors = []
    total = 0
    
    print("\n🔄 Processing cities...")
    for city, city_data in data.items():
        print(f"\n📍 {city.upper()}")
        city_total = 0
        
        # Hotels
        for hotel in city_data.get('accommodations', []):
            text = create_text('hotel', hotel, city)
            embedding = model.encode(text).tolist()
            
            vectors.append({
                'id': f"{city}_hotel_{total}",
                'values': embedding,
                'metadata': {
                    'city': city,
                    'type': 'hotel',
                    'name': hotel['name'],
                    'category': hotel.get('category', ''),
                    'price_per_night': hotel.get('price_per_night', ''),
                    'rating': str(hotel.get('rating', '')),
                    'description': hotel.get('description', '')[:500],
                    'amenities': ','.join(hotel.get('amenities', []))[:500],
                    'location': hotel.get('location', '')[:200]
                }
            })
            total += 1
            city_total += 1
        
        # Activities
        for activity in city_data.get('activities', []):
            text = create_text('activity', activity, city)
            embedding = model.encode(text).tolist()
            
            vectors.append({
                'id': f"{city}_activity_{total}",
                'values': embedding,
                'metadata': {
                    'city': city,
                    'type': 'activity',
                    'name': activity['name'],
                    'category': activity.get('category', ''),
                    'description': activity.get('description', '')[:500],
                    'entry_fee': activity.get('entry_fee', ''),
                    'opening_hours': activity.get('opening_hours', ''),
                    'best_time': activity.get('best_time', ''),
                    'duration': activity.get('duration', '')
                }
            })
            total += 1
            city_total += 1
        
        # Restaurants
        for restaurant in city_data.get('restaurants', []):
            text = create_text('restaurant', restaurant, city)
            embedding = model.encode(text).tolist()
            
            vectors.append({
                'id': f"{city}_restaurant_{total}",
                'values': embedding,
                'metadata': {
                    'city': city,
                    'type': 'restaurant',
                    'name': restaurant['name'],
                    'cuisine': restaurant.get('cuisine', ''),
                    'price_range': restaurant.get('price_range', ''),
                    'rating': str(restaurant.get('rating', '')),
                    'description': restaurant.get('description', '')[:500],
                    'specialties': ','.join(restaurant.get('specialties', []))[:500],
                    'opening_hours': restaurant.get('opening_hours', ''),
                    'reservation': restaurant.get('reservation', '')
                }
            })
            total += 1
            city_total += 1
        
        print(f"  ✓ {city_total} items")
        
        # Upload in batches
        if len(vectors) >= 100:
            index.upsert(vectors=vectors)
            print(f"  📤 Uploaded {len(vectors)} vectors")
            vectors = []
    
    # Upload remaining
    if vectors:
        index.upsert(vectors=vectors)
        print(f"  📤 Uploaded {len(vectors)} vectors")
    
    # Verify
    time.sleep(2)
    stats = index.describe_index_stats()
    
    print(f"\n{'='*60}")
    print(f"✅ MIGRATION COMPLETE!")
    print(f"📊 Total vectors in Pinecone: {stats['total_vector_count']}")
    print(f"🏙️  Cities: {len(data)}")
    print(f"📝 Items migrated: {total}")
    print(f"{'='*60}\n")
    print("✨ System is now using Pinecone vector database!")
    print("🗑️  You can delete data/travel_database.json if desired")

if __name__ == "__main__":
    try:
        migrate()
    except KeyboardInterrupt:
        print("\n⚠️  Migration interrupted!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
