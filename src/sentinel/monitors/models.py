from datetime import datetime, timezone
from enum import Enum

from sqlmodel import DateTime, Field, Relationship, SQLModel
from uuid_utils import UUID, uuid7


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


# the servies to be monitored
class Monitor(SQLModel, table=True):

    monitor_id: UUID = Field(default_factory=uuid7, primary_key=True)

    name: str

    url: str

    monitor_type: MonitorType

    check_interval: int = Field(default=60)

    timeout: int = Field(default=10)

    alert_sent: bool = Field(default=False)

    consecutive_failures: int = Field(default=0)

    current_state: CurrentState

    last_checked: datetime

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )

    logs: list["Log"] = Relationship(back_populates="monitor")

    tool_log: list["ToolLog"] = Relationship(back_populates="monitor")


# logs from the monitored services
class Log(SQLModel, table=True):
    log_id: UUID = Field(default_factory=uuid7, primary_key=True)
    monitor_id: UUID = Field(foreign_key="monitor.monitor_id")
    status: CurrentState
    response_time: int  # to be recorded in milli seconds
    status_code: int
    error_detail: str
    checked_at: datetime

    monitor: "Monitor" = Relationship(back_populates="logs")
