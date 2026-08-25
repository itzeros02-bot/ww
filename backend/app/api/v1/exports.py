"""Export functionality API endpoints."""

import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
from app.models.schemas import (
    ExportRequest,
    ExportResponse,
    ExportListResponse,
    ExportFileInfo,
    QueryAndExportRequest,
    QueryResult,
)
from app.services.export import export_service, ExportFormat

router = APIRouter(prefix="/api/v1/exports", tags=["exports"])


@router.post("/query-result", response_model=ExportResponse)
async def export_query_result(request: ExportRequest) -> ExportResponse:
    """
    Export query result to file.

    Args:
        request: Export request with format and query data

    Returns:
        Export response with file information
    """
    try:
        result = await export_service.export_query_result(
            query_result=request.queryData,
            format=request.format,
            filename=request.filename
        )

        if result.get("success"):
            # Generate download URL
            filename = os.path.basename(result["filepath"])
            download_url = f"/api/v1/exports/download/{filename}"
            return ExportResponse(
                success=True,
                filepath=result["filepath"],
                format=result["format"],
                rowCount=result.get("rowCount"),
                fileSize=result.get("fileSize"),
                downloadUrl=download_url
            )
        else:
            return ExportResponse(
                success=False,
                format=request.format,
                error=result.get("error", "Unknown error")
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )


@router.get("/download/{filename}")
async def download_export_file(filename: str):
    """
    Download exported file.

    Args:
        filename: Name of the file to download

    Returns:
        File download response
    """
    filepath = export_service.export_dir / filename

    if not filepath.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found"
        )

    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type='application/octet-stream'
    )


@router.get("/files", response_model=ExportListResponse)
async def list_export_files() -> ExportListResponse:
    """
    List all exported files.

    Returns:
        List of exported files with metadata
    """
    try:
        files = export_service.get_export_files()
        file_infos = [
            ExportFileInfo(
                filename=file["filename"],
                size=file["size"],
                createdAt=file["createdAt"],
                path=file["path"]
            )
            for file in files
        ]

        return ExportListResponse(
            files=file_infos,
            totalFiles=len(file_infos)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}"
        )


@router.delete("/files/{filename}")
async def delete_export_file(filename: str) -> dict:
    """
    Delete an exported file.

    Args:
        filename: Name of the file to delete

    Returns:
        Deletion status
    """
    filepath = export_service.export_dir / filename

    if not filepath.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found"
        )

    try:
        os.remove(filepath)
        return {"success": True, "message": f"File '{filename}' deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        )