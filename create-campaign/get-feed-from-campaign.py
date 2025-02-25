import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from witnesschain import api

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def fetch_campaign_photos(
    campaign_name: str,
    since_date: str = "2025-01-01T00:00:00Z",
    batch_size: int = 50,
    wait_seconds: int = 10
) -> None:
    """
    Continuously fetch photos from a specified campaign, with pagination and rate limiting.
    
    Args:
        campaign_name: Name of the campaign to fetch photos from
        since_date: ISO format datetime string to fetch photos from
        batch_size: Number of photos to fetch per request
        wait_seconds: Time to wait between API calls
    """
    wc_api = api()
    
    # Initial request parameters
    params = {
        "campaign": campaign_name,
        "since": since_date,
        "skip": 0,
        "limit": batch_size
    }
    
    total_photos = 0
    
    try:
        while True:
            logger.info(f"Fetching photos since {params['since']}, skip={params['skip']}, limit={params['limit']}")
            
            # Make API call to get photos
            result = wc_api.get_feed_from_campaign(params)
            
            if result and len(result) > 0:
                # Update parameters for next request
                latest_photo_date = result[0]["created_at"]
                params["since"] = latest_photo_date
                params["skip"] += batch_size

                # resetting batch size after initial processing
                batch_size = 50
                
                total_photos += len(result)
                logger.info(f"Fetched {len(result)} photos. Latest from {latest_photo_date}. Total: {total_photos}")
                
                # Process photos here
                process_photos(result)
            else:
                logger.info("No photos found or reached end of results. Resetting skip value.")
                params["skip"] = 0
            
            # Sleep to avoid hitting rate limits
            logger.debug(f"Waiting {wait_seconds} seconds before next request")
            time.sleep(wait_seconds)
            
    except KeyboardInterrupt:
        logger.info("Process manually stopped.")
    except Exception as e:
        logger.error(f"Error fetching photos: {str(e)}", exc_info=True)

def process_photos(photos: List[Dict]) -> None:
    """
    Process the fetched photos. 
    
    Args:
        photos: List of photo data dictionaries from the API
    """
    pass

if __name__ == "__main__":
    # Configuration
    CAMPAIGN_NAME = "WitnessNature"
    START_DATE = "2025-01-01T00:00:00Z"
    BATCH_SIZE = 1000
    WAIT_SECONDS = 10
    
    fetch_campaign_photos(
        campaign_name=CAMPAIGN_NAME,
        since_date=START_DATE,
        batch_size=BATCH_SIZE,
        wait_seconds=WAIT_SECONDS
    )