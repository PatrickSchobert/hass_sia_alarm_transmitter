# SIA Alarm Transmitter for Home Assistant

## Features
- Enable transmssion of event by Home assistant to an Alarm supervision system using the SIA protocol.
- Primary and backup alarm monitoring hosts
- TLS parameter support
- Configurable protocol settings
- Automatic failover mechanism

## Installation
1. Add repository to HACS
2. Install integration
3. Configure through Home Assistant UI

## Configuration
- Primary Host: Main monitoring station IP/hostname
- Primary Port: Main station port
- Backup Host (optional): Secondary monitoring station
- Backup Port: Secondary station port
- Protocol Number: 4-digit identifier
- Station ID: 4-digit receiver identifier
- Subscriber ID: 4-digit customer identifier
- Account Code: Unique identifier
