from enum import Enum


# type of request to make
class MonitorType(str, Enum):
    http: str = "http"
    tcp: str = "tcp"
    ssl: str = "ssl"


# current state of service
class CurrentState(str, Enum):
    up: str = "up"
    down: str = "down"
    unknown: str = "unknown"


# tool used
class AlertToolType(str, Enum):
    discord: str = "discord"
    slack: str = "slack"
    gmail: str = "gmail"


# tool message delivery status
class DeliveryStatus(str, Enum):
    sent: str = "sent"
    failed: str = "failed"
    retrying: str = "retrying"
