"""Intelligent automation and suggestions API endpoints."""

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Dict, Any
from app.models.schemas import QueryInput, QueryResult
from app.services.automation import intelligent_assistant, automation_workflow
from app.services.query_wrapper import execute_query_with_service
from app.models.database import DatabaseConnection
from app.database import get_session
from sqlmodel import select

router = APIRouter(prefix="/api/v1/automation", tags=["automation"])


@router.post("/analyze-query")
async def analyze_query_and_suggest(
    request_data: Dict[str, Any],
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Analyze query result and provide intelligent export suggestions.

    Request body should contain:
    {
        "database_name": "testdb",
        "sql": "SELECT * FROM users WHERE age > 25",
        "execution_time_ms": 123
    }
    """
    try:
        # Execute query first to get result
        db_name = request_data.get("database_name")
        sql = request_data.get("sql")
        execution_time_ms = request_data.get("execution_time_ms", 0)

        # Get database connection
        statement = select(DatabaseConnection).where(
            DatabaseConnection.name == db_name
        )
        connection = session.exec(statement).first()

        if not connection:
            return {
                "error": f"Database connection '{db_name}' not found",
                "suggestions": []
            }

        # Execute query
        query_result = await execute_query_with_service(
            session,
            db_name,
            connection.db_type,
            connection.url,
            sql,
        )

        # Generate intelligent suggestions
        suggestions = intelligent_assistant.generate_contextual_suggestions(
            query_result=query_result,
            database_name=db_name,
            sql=sql,
            execution_time_ms=execution_time_ms
        )

        # Add automation workflow analysis
        automation_analysis = automation_workflow.analyze_query_and_suggest_export(
            query_result=query_result,
            sql=sql
        )

        # Get recommended format safely
        export_suggestions = suggestions.get("export_suggestions", [])
        recommended_format = "csv"  # default
        if export_suggestions and len(export_suggestions) > 0:
            recommended_format = export_suggestions[0].get("recommended_format", "csv")

        return {
            "query_info": {
                "database_name": db_name,
                "row_count": query_result.row_count,
                "column_count": len(query_result.columns),
                "execution_time_ms": execution_time_ms
            },
            "intelligent_suggestions": suggestions,
            "automation_analysis": automation_analysis,
            "recommended_actions": [
                {
                    "action": "立即导出结果",
                    "endpoint": f"/api/v1/dbs/{db_name}/query-and-export",
                    "method": "POST",
                    "body": {
                        "sql": sql,
                        "exportFormat": recommended_format,
                        "filename": "auto_export_query"
                    }
                },
                {
                    "action": "查看导出历史",
                    "endpoint": f"/api/v1/exports/files",
                    "method": "GET"
                },
                {
                    "action": "分析其他查询模式",
                    "suggestion": "尝试聚合查询：SELECT COUNT(*) as total, AVG(age) as avg_age FROM users"
                }
            ]
        }

    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "suggestions": []
        }


@router.post("/auto-export-config")
async def configure_auto_export(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Configure automatic export behavior.

    Config options:
    {
        "auto_export_enabled": true,
        "auto_export_threshold": 100,  // Auto export if result has >100 rows
        "default_export_format": "csv"
    }
    """
    automation_workflow.auto_export_enabled = config.get("auto_export_enabled", True)
    automation_workflow.export_suggestions = []

    return {
        "success": True,
        "config": {
            "auto_export_enabled": automation_workflow.auto_export_enabled,
            "large_resultset_threshold": automation_workflow.query_patterns["large_resultset"]
        },
        "message": "自动导出配置已更新"
    }


@router.get("/export-suggestions")
async def get_export_suggestions() -> Dict[str, Any]:
    """
    Get current export suggestions and configuration.
    """
    return {
        "automation_config": {
            "auto_export_enabled": automation_workflow.auto_export_enabled,
            "threshold": automation_workflow.query_patterns["large_resultset"]
        },
        "active_suggestions": automation_workflow.export_suggestions,
        "user_preferences": intelligent_assistant.user_preferences
    }