from sqlmodel import DateTime, SQLModel, Field, Relationship
from uuid_utils import uuid7, UUID
from app.db.db_enums import MonitorType, CurrentState, AlertToolType, DeliveryStatus
from datetime import datetime, timezone


class Admin(SQLModel, table=True):
    user_id: UUID = Field(default_factory=uuid7, primary_key=True)
    identifier_name: str = Field(unique=True, nullable=False)
    password_hash: str


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


# app used to provide alerts
class AlertTool(SQLModel, table=True):
    __tablename__ = "alert_tool"
    tool_id: UUID = Field(default_factory=uuid7, primary_key=True)
    tool_name: AlertToolType
    webhook_url: str
    is_active: bool = Field(default=True)

    tool_log: list["ToolLog"] = Relationship(back_populates="alert_tool")


# logs of the app that sent the alert
class ToolLog(SQLModel, table=True):
    __tablename__ = "tool_log"
    log_id: UUID = Field(default_factory=uuid7, primary_key=True)

    monitor_id: UUID = Field(foreign_key="monitor.monitor_id")

    tool_id: UUID = Field(foreign_key="alert_tool.tool_id")

    delivery_state: DeliveryStatus

    retry_count: int = Field(default=0)

    fired_at: datetime

    alert_tool: "AlertTool" = Relationship(back_populates="tool_log")

    monitor: "Monitor" = Relationship(back_populates="tool_log")
