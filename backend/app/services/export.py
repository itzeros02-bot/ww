"""Export functionality services."""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import aiofiles
from app.models.schemas import QueryResult, QueryColumn


class ExportFormat:
    """Supported export formats."""
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"


class ExporterBase:
    """Base class for data exporters."""

    def __init__(self, query_result: QueryResult):
        self.query_result = query_result
        self.columns = [col.name for col in query_result.columns]
        self.rows = query_result.rows

    async def export(self, filepath: str) -> Dict[str, Any]:
        """Export data to file. To be implemented by subclasses."""
        raise NotImplementedError


class CSVExporter(ExporterBase):
    """CSV format exporter."""

    async def export(self, filepath: str) -> Dict[str, Any]:
        """Export query result to CSV file."""
        try:
            # Use regular file write instead of async to avoid potential issues
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Write header
                writer.writerow(self.columns)

                # Write data rows
                for row in self.rows:
                    # Convert dict row to list ordered by columns
                    ordered_row = [row.get(col, '') for col in self.columns]
                    writer.writerow(ordered_row)

            file_size = Path(filepath).stat().st_size
            print(f"✅ CSV export completed: {filepath} ({file_size} bytes)")

            return {
                "success": True,
                "filepath": filepath,
                "format": ExportFormat.CSV,
                "rowCount": len(self.rows),
                "fileSize": file_size
            }
        except Exception as e:
            print(f"❌ CSV export failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "format": ExportFormat.CSV
            }


class JSONExporter(ExporterBase):
    """JSON format exporter."""

    async def export(self, filepath: str) -> Dict[str, Any]:
        """Export query result to JSON file."""
        try:
            export_data = {
                "metadata": {
                    "exportedAt": datetime.now().isoformat(),
                    "totalRows": len(self.rows),
                    "columns": [{"name": col.name, "dataType": col.data_type}
                              for col in self.query_result.columns],
                    "sql": self.query_result.sql,
                    "executionTimeMs": self.query_result.execution_time_ms
                },
                "data": self.rows
            }

            # Use regular file write instead of async
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json.dumps(export_data, indent=2, ensure_ascii=False))

            file_size = Path(filepath).stat().st_size
            print(f"✅ JSON export completed: {filepath} ({file_size} bytes)")

            return {
                "success": True,
                "filepath": filepath,
                "format": ExportFormat.JSON,
                "rowCount": len(self.rows),
                "fileSize": file_size
            }
        except Exception as e:
            print(f"❌ JSON export failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "format": ExportFormat.JSON
            }


class ExcelExporter(ExporterBase):
    """Excel format exporter (simple CSV with .xlsx extension)."""

    async def export(self, filepath: str) -> Dict[str, Any]:
        """Export query result to Excel-compatible file."""
        # For simplicity, we'll use CSV format with .xlsx extension
        # In production, you'd use openpyxl or similar library
        csv_exporter = CSVExporter(self.query_result)
        result = await csv_exporter.export(filepath)

        if result.get("success"):
            result["format"] = ExportFormat.EXCEL

        return result


class ExportService:
    """Service for managing data exports."""

    def __init__(self, export_dir: str = "exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)

    def get_exporter(self, format: str, query_result: QueryResult) -> ExporterBase:
        """Get appropriate exporter for format."""
        exporters = {
            ExportFormat.CSV: CSVExporter,
            ExportFormat.JSON: JSONExporter,
            ExportFormat.EXCEL: ExcelExporter
        }

        exporter_class = exporters.get(format.lower(), CSVExporter)
        return exporter_class(query_result)

    async def export_query_result(
        self,
        query_result: QueryResult,
        format: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Export query result to file."""

        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_result_{timestamp}.{format}"

        filepath = self.export_dir / filename

        # Get appropriate exporter and export
        exporter = self.get_exporter(format, query_result)
        result = await exporter.export(str(filepath))

        return result

    def get_export_files(self) -> List[Dict[str, Any]]:
        """Get list of exported files."""
        files = []
        for file in self.export_dir.glob("*"):
            if file.is_file():
                stat = file.stat()
                files.append({
                    "filename": file.name,
                    "size": stat.st_size,
                    "createdAt": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "path": str(file)
                })
        return sorted(files, key=lambda x: x["createdAt"], reverse=True)


# Global export service instance
export_service = ExportService()