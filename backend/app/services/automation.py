"""
Automation workflow services for database query tool
Implements Agent-based workflows and intelligent export suggestions
"""

from typing import Dict, List, Any, Optional, List
from datetime import datetime
from app.services.query import save_query_history
from app.services.export import export_service, ExportFormat
from app.models.schemas import QueryResult, ExportResponse
from app.models.query import QuerySource
from sqlmodel import Session


class AutomationWorkflow:
    """Automation workflow for query and export operations"""

    def __init__(self):
        self.export_suggestions = []
        self.auto_export_enabled = True
        self.last_query_result = None
        self.query_patterns = {
            "large_resultset": 100,  # Suggest export if result has >100 rows
            "complex_query": ["JOIN", "GROUP BY", "HAVING"],  # Complex queries
            "aggregation": ["COUNT", "SUM", "AVG", "MAX", "MIN"]  # Aggregation queries
        }

    def analyze_query_and_suggest_export(
        self,
        query_result: QueryResult,
        sql: str
    ) -> Dict[str, Any]:
        """
        Analyze query result and provide intelligent export suggestions

        Args:
            query_result: Result from SQL query execution
            sql: The SQL query that was executed

        Returns:
            Dictionary with suggestions and recommendations
        """
        suggestions = {
            "should_export": False,
            "recommended_formats": [],
            "reason": "",
            "auto_export_filename": None,
            "quick_actions": []
        }

        # Rule 1: Large resultset
        if query_result.row_count > self.query_patterns["large_resultset"]:
            suggestions["should_export"] = True
            suggestions["recommended_formats"] = ["csv", "json"]
            suggestions["reason"] = f"查询返回 {query_result.row_count} 行数据，建议导出以便后续分析"
            suggestions["auto_export_filename"] = f"large_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Rule 2: Complex queries
        sql_upper = sql.upper()
        for pattern in self.query_patterns["complex_query"]:
            if pattern in sql_upper:
                suggestions["should_export"] = True
                suggestions["recommended_formats"].append("csv")
                suggestions["reason"] += f" 查询包含 {pattern} 操作，结果值得保存"
                break

        # Rule 3: Aggregation queries
        for agg in self.query_patterns["aggregation"]:
            if agg in sql_upper:
                suggestions["should_export"] = True
                suggestions["recommended_formats"].append("json")
                suggestions["reason"] += f" 查询包含 {agg} 聚合函数，适合报表导出"

        # Remove duplicates and sort
        suggestions["recommended_formats"] = list(set(suggestions["recommended_formats"]))

        # Generate quick actions
        if suggestions["should_export"]:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            suggestions["quick_actions"] = [
                {
                    "action": "导出为CSV",
                    "format": "csv",
                    "filename": f"query_export_{timestamp}.csv",
                    "api_endpoint": "/api/v1/dbs/{db}/query-and-export",
                    "auto_trigger": True
                },
                {
                    "action": "导出为JSON",
                    "format": "json",
                    "filename": f"query_export_{timestamp}.json",
                    "api_endpoint": "/api/v1/dbs/{db}/query-and-export",
                    "auto_trigger": True
                }
            ]

        return suggestions

    async def auto_export_after_query(
        self,
        session: Session,
        database_name: str,
        db_type: str,
        url: str,
        sql: str,
        query_result: QueryResult
    ) -> Optional[ExportResponse]:
        """
        Automatically export after query if conditions are met

        Args:
            session: Database session
            database_name: Database connection name
            db_type: Database type
            url: Database URL
            sql: SQL query
            query_result: Query result

        Returns:
            ExportResponse if auto-export was triggered, None otherwise
        """
        if not self.auto_export_enabled:
            return None

        suggestions = self.analyze_query_and_suggest_export(query_result, sql)

        # Auto-export if strongly suggested
        if suggestions["should_export"] and query_result.row_count > 50:
            # Use first recommended format
            export_format = suggestions["recommended_formats"][0]
            filename = suggestions.get("auto_export_filename")

            result = await export_service.export_query_result(
                query_result=query_result,
                format=export_format,
                filename=filename
            )

            if result.get("success"):
                return ExportResponse(
                    success=True,
                    filepath=result["filepath"],
                    format=result["format"],
                    rowCount=result.get("rowCount"),
                    fileSize=result.get("fileSize"),
                    downloadUrl=f"/api/v1/exports/download/{filename}"
                )

        return None


class IntelligentAssistant:
    """AI Assistant for providing proactive suggestions"""

    def __init__(self):
        self.suggestions_history = []
        self.user_preferences = {
            "default_export_format": "csv",
            "auto_export_threshold": 100,
            "favorite_formats": []
        }

    def generate_contextual_suggestions(
        self,
        query_result: QueryResult,
        database_name: str,
        sql: str,
        execution_time_ms: int
    ) -> Dict[str, Any]:
        """
        Generate intelligent suggestions based on query context

        Args:
            query_result: Query execution result
            database_name: Database name
            sql: SQL query string
            execution_time_ms: Query execution time in milliseconds

        Returns:
            Dictionary with contextual suggestions
        """
        context = {
            "database_name": database_name,
            "query_summary": self._summarize_query(sql),
            "result_stats": {
                "row_count": query_result.row_count,
                "column_count": len(query_result.columns),
                "execution_time": f"{execution_time_ms}ms"
            },
            "export_suggestions": [],
            "follow_up_actions": []
        }

        # Analyze query characteristics
        query_characteristics = self._analyze_query_characteristics(sql, query_result)

        # Generate export suggestions based on characteristics
        if query_characteristics["is_large_dataset"]:
            context["export_suggestions"].append({
                "message": f"🎯 查询返回 {query_result.row_count} 行数据，建议导出为CSV格式进行进一步分析",
                "recommended_format": "csv",
                "reason": "large_dataset"
            })

        if query_characteristics["is_analytical_query"]:
            context["export_suggestions"].append({
                "message": "📊 这是一个分析查询，结果适合导出为JSON格式用于报告",
                "recommended_format": "json",
                "reason": "analytical"
            })

        if query_characteristics["is_complex_join"]:
            context["export_suggestions"].append({
                "message": "🔗 查询涉及多表关联，建议导出结果以便分享",
                "recommended_format": "csv",
                "reason": "complex_join"
            })

        # Generate follow-up action suggestions
        context["follow_up_actions"] = [
            {
                "action": "查看数据模式",
                "suggestion": f"SHOW TABLES; DESCRIBE users;",
                "reason": "了解数据库结构"
            },
            {
                "action": "执行聚合分析",
                "suggestion": f"SELECT COUNT(*) as total, AVG(age) as avg_age FROM users;",
                "reason": "获取统计信息"
            },
            {
                "action": "数据导出",
                "suggestion": "将当前查询结果导出为文件",
                "reason": "保存分析结果"
            }
        ]

        return context

    def _summarize_query(self, sql: str) -> str:
        """Generate a natural language summary of the SQL query"""
        sql_upper = sql.upper().strip()

        if "COUNT" in sql_upper or "SUM" in sql_upper or "AVG" in sql_upper:
            return "这是一个聚合分析查询"
        elif "JOIN" in sql_upper:
            return "这是一个多表关联查询"
        elif "ORDER BY" in sql_upper:
            return "这是一个排序查询"
        elif "WHERE" in sql_upper:
            return "这是一个条件过滤查询"
        else:
            return "这是一个基础查询"

    def _analyze_query_characteristics(
        self,
        sql: str,
        query_result: QueryResult
    ) -> Dict[str, Any]:
        """Analyze query characteristics for intelligent suggestions"""
        characteristics = {
            "is_large_dataset": query_result.row_count > 100,
            "is_analytical_query": any(
                keyword in sql.upper()
                for keyword in ["COUNT", "SUM", "AVG", "MAX", "MIN", "GROUP BY"]
            ),
            "is_complex_join": sql.upper().count("JOIN") > 1,
            "has_aggregation": "GROUP BY" in sql.upper(),
            "involves_multiple_tables": len(sql.upper().split("FROM")) > 2
        }

        return characteristics


# Global instances
automation_workflow = AutomationWorkflow()
intelligent_assistant = IntelligentAssistant()