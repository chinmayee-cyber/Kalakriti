import time
from typing import Dict, List, Optional
from tqdm import tqdm

# Import from our modules
from config.settings import Config
from core.clip_classifier import CLIPClassifier
from core.image_processor import ImageProcessor
from database.mongodb_handler import MongoDBHandler
from models.metadata_models import generate_caption, create_metadata_dict
from utils.helpers import (
    setup_logging, download_image_sync, process_batch, create_mongodb_indexes
)

logger = setup_logging()

class ArtMetadataGenerator:
    """Main metadata generator with optimizations"""
    
    def __init__(self):
        # MongoDB setup
        self.db_handler = MongoDBHandler()
        
        # Initialize CLIP classifier
        self.classifier = CLIPClassifier()
    
    def process_single_image(self, doc: Dict) -> Optional[Dict]:
        """
        Process a single document - optimized
        
        Args:
            doc: Document from MongoDB
            
        Returns:
            Processed document with metadata or None if processing fails
        """
        try:
            # Download image
            image = download_image_sync(doc['img_url'])
            if image is None:
                return None
            
            # Resize for faster processing
            image = ImageProcessor.resize_image_for_clip(image)
            
            # Parallel classification
            style_labels = self.classifier.classify_fast(image, 'style', 2)
            subject_labels = self.classifier.classify_fast(image, 'subject', 2)
            foreground_objects = self.classifier.classify_fast(image, 'objects', 3)
            lighting = self.classifier.classify_fast(image, 'lighting', 1)[0]
            texture = self.classifier.classify_fast(image, 'texture', 1)[0]
            background = self.classifier.classify_fast(image, 'background', 1)[0]
            
            # Fast color extraction
            img_array = np.array(image).reshape(-1, 3)
            img_hash = hash(img_array.tobytes())
            dominant_colors = list(ImageProcessor.get_dominant_colors_fast(img_hash, img_array.tobytes()))
            
            # Get embedding
            image_embedding = self.classifier.get_image_embedding(image)
            
            # Generate caption
            caption = generate_caption(style_labels, subject_labels, doc.get('medium', 'painting'))
            
            # Calculate aspect ratio
            width, height = image.size
            aspect_ratio = f"{round(width/height, 1)}:1" if width >= height else f"1:{round(height/width, 1)}"
            
            # Create metadata
            metadata = create_metadata_dict(
                caption, style_labels, doc.get('medium', 'Unknown'), dominant_colors,
                foreground_objects, background, aspect_ratio, image_embedding, texture, lighting
            )
            
            return {"_id": doc["_id"], "metadata": metadata}
            
        except Exception as e:
            logger.error(f"Error processing {doc.get('_id')}: {e}")
            return None
    
    def bulk_update_mongodb(self, results: List[Dict]):
        """
        Efficient bulk update to MongoDB
        
        Args:
            results: List of processed results to update
        """
        if not results:
            return
        
        operations = []
        for result in results:
            if result:
                operations.append(
                    pymongo.UpdateOne(
                        {"_id": result["_id"]},
                        {"$set": {"metadata": result["metadata"]}}
                    )
                )
        
        if operations:
            try:
                self.db_handler.bulk_write(operations, ordered=False)
                logger.info(f"Updated {len(operations)} documents in MongoDB")
            except Exception as e:
                logger.error(f"Bulk update error: {e}")
    
    def process_collection(self, limit: Optional[int] = None):
        """
        Main processing function with optimizations
        
        Args:
            limit: Maximum number of documents to process
        """
        # Get documents without metadata
        query = {"metadata": {"$exists": False}}
        total_docs = self.db_handler.count_documents(query)
        
        if limit:
            total_docs = min(total_docs, limit)
        
        logger.info(f"Processing {total_docs} documents with {Config.MAX_WORKERS} workers...")
        
        cursor = self.db_handler.find(query, {"_id": 1, "img_url": 1, "medium": 1})
        if limit:
            cursor = cursor.limit(limit)
        
        # Process in batches
        batch = []
        processed = 0
        
        with tqdm(total=total_docs, desc="Processing images") as pbar:
            for doc in cursor:
                batch.append(doc)
                
                if len(batch) >= Config.BATCH_SIZE:
                    # Process batch in parallel
                    results = process_batch(batch, self.process_single_image)
                    
                    # Bulk update MongoDB
                    self.bulk_update_mongodb([r for r in results if r])
                    
                    processed += len(batch)
                    pbar.update(len(batch))
                    batch = []
                    
                    # Brief pause to prevent overwhelming
                    time.sleep(0.05)
            
            # Process remaining batch
            if batch:
                results = process_batch(batch, self.process_single_image)
                self.bulk_update_mongodb([r for r in results if r])
                processed += len(batch)
                pbar.update(len(batch))
        
        logger.info(f"Processing complete! Processed {processed} documents")
    
    def create_indexes(self):
        """Create MongoDB indexes for better query performance"""
        create_mongodb_indexes(self.db_handler.collection)

def main():
    """Optimized main function"""
    logger.info("Starting art metadata generation...")
    
    generator = ArtMetadataGenerator()
    
    # Create indexes first
    generator.create_indexes()
    
    # Process collection (remove limit for full processing)
    generator.process_collection(limit=None)  # Set to None for all 968 images
    
    logger.info("✅ Metadata generation complete!")

if __name__ == "__main__":
    import pymongo  # Import here to avoid circular imports
    main()