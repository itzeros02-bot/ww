/** Query execution page with SQL editor and result table. */

import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, Button, Space, Spin, Alert, List, Typography, message, Modal, Tag } from "antd";
import { PlayCircleOutlined, ReloadOutlined, DownloadOutlined, BulbOutlined } from "@ant-design/icons";
import { apiClient } from "../../services/api";
import { QueryResult, QueryHistoryEntry, QueryInput } from "../../types/query";
import { SqlEditor } from "../../components/SqlEditor";
import { ResultTable } from "../../components/ResultTable";

const { Text } = Typography;

export const QueryExecute: React.FC = () => {
  const { databaseName } = useParams<{ databaseName: string }>();
  const [sql, setSql] = useState("SELECT * FROM ");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<QueryHistoryEntry[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState<any>(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<string | null>(null);

  useEffect(() => {
    if (databaseName) {
      loadHistory();
    }
  }, [databaseName]);

  const loadHistory = async () => {
    if (!databaseName) return;

    setLoadingHistory(true);
    try {
      const response = await apiClient.get<QueryHistoryEntry[]>(
        `/api/v1/dbs/${databaseName}/history`
      );
      setHistory(response.data);
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleExecute = async () => {
    if (!databaseName || !sql.trim()) {
      setError("Please enter a SQL query");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setAiSuggestions(null);

    try {
      const input: QueryInput = { sql: sql.trim() };
      const response = await apiClient.post<QueryResult>(
        `/api/v1/dbs/${databaseName}/query`,
        input
      );
      setResult(response.data);

      // Get AI assistant suggestions
      try {
        const analysisResponse = await apiClient.post<any>(
          `/api/v1/automation/analyze-query`,
          {
            database_name: databaseName,
            sql: sql.trim(),
            execution_time_ms: response.data.executionTimeMs || 0
          }
        );
        setAiSuggestions(analysisResponse.data);

        // Show AI suggestion if export is recommended
        if (analysisResponse.data?.automation_analysis?.should_export) {
          const reason = analysisResponse.data.automation_analysis.reason;
          const formats = analysisResponse.data.automation_analysis.recommended_formats?.join(', ') || 'CSV, JSON';
          message.success({
            content: `🤖 AI Assistant: ${reason}. 推荐格式: ${formats}`,
            duration: 5,
          });
          setShowExportModal(true);
        }
      } catch (analysisError) {
        console.warn("Failed to get AI suggestions:", analysisError);
        // Don't fail the query if analysis fails
      }

      // Reload history after successful query
      await loadHistory();
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || err.message || "Query execution failed";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleHistoryClick = (historyItem: QueryHistoryEntry) => {
    setSql(historyItem.sqlText);
    setError(null);
    setResult(null);
    setAiSuggestions(null);
  };

  const handleQuickExport = async (format: string = 'csv') => {
    if (!databaseName || !sql.trim()) {
      message.error("No query to export");
      return;
    }

    setExporting(true);
    setExportFormat(format);

    try {
      message.loading({ content: `📤 Exporting as ${format.toUpperCase()}...`, key: 'export', duration: 0 });

      const response = await apiClient.post<any>(
        `/api/v1/dbs/${databaseName}/query-and-export`,
        {
          sql: sql.trim(),
          exportFormat: format,
          filename: `query_export_${Date.now()}`
        }
      );

      if (response.data.success) {
        message.success({ content: `✅ Successfully exported as ${format.toUpperCase()}!`, key: 'export', duration: 3 });

        // Trigger download
        const downloadUrl = `http://localhost:8000${response.data.downloadUrl}`;
        window.open(downloadUrl, '_blank');

        // Update AI suggestions to reflect successful export
        if (aiSuggestions) {
          setAiSuggestions({
            ...aiSuggestions,
            last_export: {
              format: format,
              timestamp: new Date().toISOString(),
              success: true,
              download_url: downloadUrl
            }
          });
        }
      } else {
        message.error({ content: `Export failed: ${response.data.error || 'Unknown error'}`, key: 'export', duration: 5 });
      }
    } catch (err: any) {
      message.error({ content: `Export failed: ${err.response?.data?.detail || err.message || 'Unknown error'}`, key: 'export', duration: 5 });
    } finally {
      setExporting(false);
      setExportFormat(null);
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <Card
        title={`Execute Query - ${databaseName}`}
        extra={
          <Space>
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleExecute}
              loading={loading}
            >
              Execute
            </Button>
            <Button
              icon={<ReloadOutlined />}
              onClick={loadHistory}
              loading={loadingHistory}
            >
              Refresh History
            </Button>
          </Space>
        }
      >
        <Space direction="vertical" style={{ width: "100%" }} size="large">
          <div>
            <Card title="SQL Editor" size="small">
              <SqlEditor value={sql} onChange={(val) => setSql(val || "")} height="200px" />
            </Card>
          </div>

          {error && (
            <Alert
              message="Error"
              description={error}
              type="error"
              showIcon
              closable
              onClose={() => setError(null)}
            />
          )}

          {loading && (
            <div style={{ textAlign: "center", padding: "50px" }}>
              <Spin size="large" />
            </div>
          )}

          {result && (
            <>
              <Card title="Query Results" size="small">
                <ResultTable result={result} loading={loading} />
              </Card>

              {/* AI Assistant Suggestions */}
              {aiSuggestions && (
                <Card
                  title={
                    <Space>
                      <BulbOutlined style={{ color: '#faad14' }} />
                      AI Assistant Suggestions
                    </Space>
                  }
                  style={{ marginTop: 16, backgroundColor: '#fafafa' }}
                  size="small"
                >
                  <Space direction="vertical" style={{ width: '100%' }}>
                    {/* Intelligent Export Suggestions */}
                    {aiSuggestions.intelligent_suggestions?.export_suggestions?.length > 0 && (
                      <div>
                        <Text strong>💡 Export Suggestions:</Text>
                        <List
                          dataSource={aiSuggestions.intelligent_suggestions.export_suggestions}
                          renderItem={(suggestion: any) => (
                            <List.Item>
                              <Space>
                                <Tag color="blue">{suggestion.recommended_format?.toUpperCase()}</Tag>
                                <Text>{suggestion.message}</Text>
                              </Space>
                            </List.Item>
                          )}
                        />
                      </div>
                    )}

                    {/* Automation Analysis */}
                    {aiSuggestions.automation_analysis && (
                      <div>
                        <Text strong>⚙️ Analysis:</Text>
                        <Space direction="vertical" style={{ marginTop: 8 }}>
                          <Text>• Should export: {aiSuggestions.automation_analysis.should_export ? '✅ Yes' : '❌ No'}</Text>
                          {aiSuggestions.automation_analysis.reason && (
                            <Text>• Reason: {aiSuggestions.automation_analysis.reason}</Text>
                          )}
                          {aiSuggestions.automation_analysis.recommended_formats?.length > 0 && (
                            <Text>• Recommended formats: {aiSuggestions.automation_analysis.recommended_formats.join(', ')}</Text>
                          )}
                        </Space>
                      </div>
                    )}

                    {/* Quick Actions */}
                    <div>
                      <Text strong>🚀 Quick Actions:</Text>
                      <Space style={{ marginTop: 8 }}>
                        <Button
                          type="primary"
                          icon={<DownloadOutlined />}
                          onClick={() => handleQuickExport('csv')}
                          size="small"
                          loading={exporting && exportFormat === 'csv'}
                        >
                          Export as CSV
                        </Button>
                        <Button
                          icon={<DownloadOutlined />}
                          onClick={() => handleQuickExport('json')}
                          size="small"
                          loading={exporting && exportFormat === 'json'}
                        >
                          Export as JSON
                        </Button>
                      </Space>
                      {aiSuggestions.last_export && (
                        <div style={{ marginTop: 8 }}>
                          <Text type="success" style={{ fontSize: '12px' }}>
                            ✅ Last export: {aiSuggestions.last_export.format.toUpperCase()} at {new Date(aiSuggestions.last_export.timestamp).toLocaleTimeString()}
                          </Text>
                        </div>
                      )}
                    </div>
                  </Space>
                </Card>
              )}
            </>
          )}
        </Space>
      </Card>

      <Card title="Query History" style={{ marginTop: 16 }}>
        {loadingHistory ? (
          <Spin />
        ) : (
          <List
            dataSource={history}
            renderItem={(item) => (
              <List.Item
                style={{
                  cursor: "pointer",
                  backgroundColor: item.success ? "transparent" : "#fff2f0",
                }}
                onClick={() => handleHistoryClick(item)}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Text
                        code
                        style={{
                          maxWidth: "600px",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                          display: "inline-block",
                        }}
                      >
                        {item.sqlText}
                      </Text>
                      {item.success ? (
                        <Text type="success">
                          ✓ {item.rowCount} rows in {item.executionTimeMs}ms
                        </Text>
                      ) : (
                        <Text type="danger">✗ Failed</Text>
                      )}
                    </Space>
                  }
                  description={
                    <Text type="secondary">
                      {new Date(item.executedAt).toLocaleString()}
                    </Text>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>
    </div>
  );
};
