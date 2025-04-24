import logging
import asyncio
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def async_setup_send_event_service(hass: HomeAssistant):
    """Register the send_event service for SIA Alarm Transmitter."""

    async def handle_send_event(call: ServiceCall):
        account_id = call.data.get("account_id")
        event_code = call.data.get("code", "BA")
        zone = call.data.get("zone", 1)
        area = call.data.get("area", 1)
        message = call.data.get("message", "SIA Event")

        # Build the SIA DC-09 message (MSD-compatible with STX/ETX framing)
        payload = f"[{event_code}{int(zone):04d}|{message}]"
        body = f"#{account_id}{payload}"
        length = len(body)
        sia_core = f'"SIA-DCS"{length:04d}L0{body}\r\n'
        sia_message = f"\x02{sia_core}\x03"

        # Optional Logging
        _LOGGER.info("SIA-Nachricht (framed): %s", repr(sia_message))

        # Send via TCP (make sure target host/port is configured or fixed here)
        try:
            reader, writer = await asyncio.open_connection("127.0.0.1", 5000)
            writer.write(sia_message.encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            _LOGGER.info("SIA-Nachricht erfolgreich gesendet.")
        except Exception as e:
            _LOGGER.error("Fehler beim Senden der SIA-Nachricht: %s", e)

    hass.services.async_register(
        "sia_alarm_transmitter",
        "send_event",
        handle_send_event
    )
