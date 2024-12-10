"""Enhanced SIA Protocol Communication Handler with TLS Parameters."""
import logging
import asyncio
import socket

LOGGER = logging.getLogger(__name__)

class SIAProtocolHandler:
    """Handles SIA protocol communication with TLS parameters."""
    def __init__(self, 
                 primary_host, 
                 primary_port=5051, 
                 backup_host=None, 
                 backup_port=5051, 
                 timeout=10, 
                 retry_attempts=2,
                 protocol_number='6678',
                 station_id='0000',
                 subscriber_id='0000',
                 account_code='1234556'):
        """
        Initialize SIA protocol handler with TLS parameters.
        
        :param station_id: 4-digit station/receiver identifier
        :param subscriber_id: 4-digit subscriber/customer identifier
        """
        self.primary_host = primary_host
        self.primary_port = primary_port
        self.backup_host = backup_host
        self.backup_port = backup_port
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.protocol_number = protocol_number
        self.station_id = station_id
        self.subscriber_id = subscriber_id
        self.account_code = account_code

    async def send_sia_message(self, event_code, account_code, message):
        """
        Send SIA message with TLS parameters.
        """
        # Construct full SIA message with protocol and TLS specifics
        sia_message_parts = [
            f"[{self.protocol_number}",     # Protocol number
            f"01{len(message):02d}{event_code}0]",  # Standard SIA header
            f"R{self.station_id}",          # Station/Receiver ID
            f"S{self.subscriber_id}",       # Subscriber ID
            f"{self.account_code}",              # Account code
            f"{message}"                    # Message content
        ]
        
        sia_message = ''.join(sia_message_parts)
        
        # Existing failover logic
        try:
            return await self._send_to_host(
                self.primary_host, 
                self.primary_port, 
                sia_message
            )
        except Exception as primary_error:
            LOGGER.warning(f"Primary host failed: {primary_error}")
            
            if self.backup_host:
                try:
                    return await self._send_to_host(
                        self.backup_host, 
                        self.backup_port, 
                        sia_message
                    )
                except Exception as backup_error:
                    LOGGER.error(f"Backup host also failed: {backup_error}")
            
            return False

    async def _send_to_host(self, host, port, message):
        """Low-level message transmission with retry mechanism."""
        for attempt in range(self.retry_attempts + 1):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port), 
                    timeout=self.timeout
                )
                
                writer.write(message.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                
                LOGGER.info(f"SIA message sent to {host}:{port}")
                return True
            
            except (socket.error, asyncio.TimeoutError) as err:
                if attempt < self.retry_attempts:
                    LOGGER.warning(f"Transmission attempt {attempt + 1} failed: {err}")
                    await asyncio.sleep(1)
                else:
                    raise
