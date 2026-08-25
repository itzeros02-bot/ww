"""API request/response schemas with camelCase aliases."""

from pydantic import BaseModel, Field
from typing import Literal, Any, Optional, List, Dict
from datetime import datetime
from app.models.query import QuerySource


# Database Connection Schemas
class DatabaseConnectionInput(BaseModel):
    """Input schema for creating/updating database connection."""

    url: str = Field(..., description="Database connection URL (PostgreSQL or MySQL)")
    db_type: Optional[str] = Field(default=None, alias="dbType", description="Database type (postgresql or mysql). Auto-detected from URL if not provided.")
    description: Optional[str] = Field(default=None, max_length=200)


class DatabaseConnectionResponse(BaseModel):
    """Response schema for database connection."""

    name: str
    url: str
    db_type: str = Field(..., alias="dbType")
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_connected_at: Optional[datetime]
    status: str


# Metadata Schemas
class ColumnMetadata(BaseModel):
    """Column metadata schema."""

    name: str = Field(..., max_length=63)
    data_type: str = Field(..., alias="dataType")
    nullable: bool
    primary_key: bool = Field(..., alias="primaryKey")
    unique: bool = False
    default_value: Optional[str] = Field(default=None, alias="defaultValue")
    comment: Optional[str] = None


class TableMetadata(BaseModel):
    """Table/View metadata schema."""

    name: str = Field(..., max_length=63)
    type: Literal["table", "view"]
    columns: List[ColumnMetadata]
    row_count: Optional[int] = Field(default=None, alias="rowCount")
    schema_name: str = Field(default="public", alias="schemaName")


class DatabaseMetadataResponse(BaseModel):
    """Response schema for database metadata."""

    database_name: str = Field(..., alias="databaseName")
    tables: List[TableMetadata]
    views: List[TableMetadata]
    fetched_at: datetime = Field(..., alias="fetchedAt")
    is_stale: bool = Field(..., alias="isStale")


# Query Schemas
class QueryInput(BaseModel):
    """Input schema for SQL query execution."""

    sql: str = Field(..., min_length=1, description="SQL SELECT query to execute")


class QueryColumn(BaseModel):
    """Query result column schema."""

    name: str
    data_type: str = Field(..., alias="dataType")


class QueryResult(BaseModel):
    """Query result response schema."""

    columns: List[QueryColumn]
    rows: List[Dict[str, Any]]
    row_count: int = Field(..., alias="rowCount")
    execution_time_ms: int = Field(..., alias="executionTimeMs")
    sql: str


class QueryHistoryEntry(BaseModel):
    """Query history entry schema."""

    id: int
    database_name: str = Field(..., alias="databaseName")
    sql_text: str = Field(..., alias="sqlText")
    executed_at: datetime = Field(..., alias="executedAt")
    execution_time_ms: Optional[int] = Field(None, alias="executionTimeMs")
    row_count: Optional[int] = Field(None, alias="rowCount")
    success: bool
    error_message: Optional[str] = Field(None, alias="errorMessage")
    query_source: str = Field(..., alias="querySource")


# Natural Language Schemas
class NaturalLanguageInput(BaseModel):
    """Input schema for natural language to SQL conversion."""

    prompt: str = Field(..., min_length=5, max_length=500)


class GeneratedSqlResponse(BaseModel):
    """Response schema for generated SQL."""

    sql: str
    explanation: str


# Error Schema
class ErrorResponse(BaseModel):
    """Error response schema."""

    error: Dict[str, Any]


# Export Schemas
class ExportRequest(BaseModel):
    """Input schema for exporting query results."""

    format: str = Field(..., pattern="^(csv|json|excel)$", description="Export format: csv, json, or excel")
    filename: Optional[str] = Field(None, max_length=255, description="Custom filename (without extension)")
    queryData: QueryResult


class ExportResponse(BaseModel):
    """Response schema for export operations."""

    success: bool
    filepath: Optional[str] = Field(None, description="Path to exported file")
    format: str = Field(..., description="Export format used")
    rowCount: Optional[int] = Field(None, description="Number of rows exported")
    fileSize: Optional[int] = Field(None, description="Size of exported file in bytes")
    error: Optional[str] = Field(None, description="Error message if export failed")
    downloadUrl: Optional[str] = Field(None, description="URL to download exported file")


class ExportFileInfo(BaseModel):
    """Export file information schema."""

    filename: str
    size: int
    createdAt: str
    path: str


class ExportListResponse(BaseModel):
    """Response schema for export files list."""

    files: List[ExportFileInfo]
    totalFiles: int


class QueryAndExportRequest(BaseModel):
    """Input schema for combined query and export operation."""

    sql: str = Field(..., min_length=1, description="SQL SELECT query to execute")
    exportFormat: str = Field(..., pattern="^(csv|json|excel)$", description="Export format: csv, json, or excel")
    filename: Optional[str] = Field(None, max_length=255, description="Custom filename (without extension)")
