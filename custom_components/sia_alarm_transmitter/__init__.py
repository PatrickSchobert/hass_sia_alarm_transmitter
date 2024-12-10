"""Home Assistant SIA Alarm Transmitter"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config):
    """Set up the SIA Alarm Transmitter."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up configuration entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Setup SIA Protocol Handler with TLS parameters
    from .sia_protocol import SIAProtocolHandler
    sia_handler = SIAProtocolHandler(
        primary_host=entry.data['primary_host'],
        primary_port=entry.data.get('primary_port', 5051),
        backup_host=entry.data.get('backup_host'),
        backup_port=entry.data.get('backup_port', 5051),
        protocol_number=entry.data.get('protocol_number', '6678'),
        station_id=entry.data.get('station_id', '0000'),
        subscriber_id=entry.data.get('subscriber_id', '0000'),
        account_code=entry.data.get('account_code', '9999')
    )
    
    # Store handler for later use
    hass.data[DOMAIN][entry.entry_id] = sia_handler
    
    # Register services
    async def send_alarm_event(call):
        """Service to send alarm events."""
        event_code = call.data.get('event_code', 'BA')
        account_code = call.data.get('account_code')
        message = call.data.get('message', '')
        
        await sia_handler.send_sia_message(event_code, account_code, message)
    
    hass.services.async_register(DOMAIN, 'send_event', send_alarm_event)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload configuration entry."""
    hass.services.async_remove(DOMAIN, 'send_event')
    
    # Remove stored handler
    hass.data[DOMAIN].pop(entry.entry_id, None)
    
    return True
