from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
from uuid_utils import UUID, uuid7


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
