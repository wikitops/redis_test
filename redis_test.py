import os
import sys
import logging
import socket

from redis import Redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_port_connection(host, port, timeout=5):
    """Test if we can establish a TCP connection to the specified host and port"""
    try:
        logger.info(f"Testing TCP connection to {host}:{port}")
        with socket.create_connection((host, port), timeout=timeout):
            logger.info(f"✅ Port connection test: SUCCESS - {host}:{port} is reachable")
            return True
    except socket.timeout:
        logger.error(f"❌ Port connection test: FAILED - Connection timeout to {host}:{port}")
        return False
    except ConnectionRefusedError:
        logger.error(f"❌ Port connection test: FAILED - Connection refused by {host}:{port}")
        return False
    except socket.gaierror as e:
        logger.error(f"❌ Port connection test: FAILED - Host resolution error for {host}:{port} - {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Port connection test: FAILED - Unexpected error: {str(e)}")
        return False


def test_redis_connection():
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    
    if not redis_host:
        logger.error("REDIS_HOST environment variable not set")
        return False
    
    logger.info(f"Testing connection to Redis at {redis_host}:{redis_port}")
    
    if not test_port_connection(redis_host, redis_port):
        logger.error("Skipping Redis protocol test due to port connection failure")
        return False

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