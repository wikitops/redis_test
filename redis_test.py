import os
import sys
import logging

from redis import Redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_redis_connection():
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    
    if not redis_host:
        logger.error("REDIS_HOST environment variable not set")
        return False
    
    logger.info(f"Testing connection to Redis at {redis_host}:{redis_port}")
    
    try:
        redis_client = Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
            socket_connect_timeout=10,
            socket_keepalive=True
        )
        
        logger.info("Sending PING command...")
        response = redis_client.ping()
        logger.info(f"PING response: {response}")
        
        logger.info("✅ Redis connection test: SUCCESS")
        return True
        
    except Exception as e:
        logger.error(f"❌ Redis connection test: FAILED - {str(e)}")
        return False

if __name__ == '__main__':
    success = test_redis_connection()
    sys.exit(0 if success else 1)