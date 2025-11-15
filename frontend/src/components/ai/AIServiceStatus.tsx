import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
  Grid
} from '@mui/material';
import { CheckCircle, Error, Info, Refresh } from '@mui/icons-material';
import aiService from '../../services/aiService';
import { AIServiceStatus as AIServiceStatusType } from '../../types/ai';

interface AIServiceStatusProps {
  autoRefresh?: boolean;
  refreshInterval?: number; // 毫秒
  showDetailedInfo?: boolean;
}

const AIServiceStatus: React.FC<AIServiceStatusProps> = ({
  autoRefresh = true,
  refreshInterval = 60000, // 默认1分钟刷新一次
  showDetailedInfo = true
}) => {
  const [status, setStatus] = useState<AIServiceStatusType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStatus = async () => {
    try {
      setError(null);
      const data = await aiService.getAIServiceStatus();
      setStatus(data);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '获取AI服务状态失败'
      );
      // 设置一个默认的错误状态
      setStatus({
        status: 'unavailable',
        service_name: 'AI Recipe Service',
        version: 'unknown',
        uptime: 0,
        current_load: 100,
        max_concurrent_requests: 0,
        active_requests: 0,
        features: {
          recipe_generation: false,
          recipe_enhancement: false,
          nutrition_analysis: false,
          ingredient_suggestion: false
        },
        message: '服务暂时不可用'
      });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchStatus();
  };

  useEffect(() => {
    fetchStatus();

    // 设置自动刷新
    if (autoRefresh) {
      const interval = setInterval(fetchStatus, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <CircularProgress size={16} />
        <Typography variant="body2">正在检查AI服务状态...</Typography>
      </Box>
    );
  }

  const getStatusChip = () => {
    if (!status) return null;

    switch (status.status) {
      case 'operational':
        return (
          <Chip
            icon={<CheckCircle fontSize="small" />}
            label="服务正常"
            color="success"
            size="small"
          />
        );
      case 'degraded':
        return (
          <Chip
            icon={<Info fontSize="small" />}
            label="性能下降"
            color="warning"
            size="small"
          />
        );
      case 'unavailable':
        return (
          <Chip
            icon={<Error fontSize="small" />}
            label="服务不可用"
            color="error"
            size="small"
          />
        );
      default:
        return (
          <Chip
            icon={<Info fontSize="small" />}
            label="未知状态"
            color="default"
            size="small"
          />
        );
    }
  };

  const getLoadPercentage = () => {
    if (!status) return 0;
    if (status.max_concurrent_requests === 0) return 100;
    return Math.round((status.active_requests / status.max_concurrent_requests) * 100);
  };

  const getLoadColor = () => {
    const load = getLoadPercentage();
    if (load > 80) return 'error.main';
    if (load > 60) return 'warning.main';
    return 'success.main';
  };

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (days > 0) {
      return `${days}天 ${hours}小时`;
    } else if (hours > 0) {
      return `${hours}小时 ${minutes}分钟`;
    } else {
      return `${minutes}分钟`;
    }
  };

  const FeatureStatus = ({ featureName, available }: { featureName: string; available: boolean }) => (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
      <CheckCircle 
        fontSize="small" 
        color={available ? "success" : "error"} 
      />
      <Typography variant="body2">
        {available ? `${featureName}` : `${featureName} (不可用)`}
      </Typography>
    </Box>
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
        <Typography variant="subtitle2" fontWeight="medium">
          AI服务状态:
        </Typography>
        {getStatusChip()}
        <Tooltip title="刷新服务状态">
          <Refresh 
            fontSize="small" 
            color="action" 
            onClick={handleRefresh}
            sx={{ cursor: 'pointer', opacity: refreshing ? 0.5 : 1 }}
          />
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="error" variant="outlined" size="small" sx={{ mb: 2 }}>
          <Typography variant="caption">{error}</Typography>
        </Alert>
      )}

      {showDetailedInfo && status && (
        <Box sx={{ p: 1.5, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
            服务详情:
          </Typography>
          <Grid container spacing={1}>
            <Grid item xs={6}>
              <Typography variant="caption">版本:</Typography>
              <Typography variant="body2">{status.version}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="caption">运行时间:</Typography>
              <Typography variant="body2">{formatUptime(status.uptime)}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="caption">当前负载:</Typography>
              <Typography variant="body2" sx={{ color: getLoadColor() }}>
                {getLoadPercentage()}% ({status.active_requests}/{status.max_concurrent_requests})
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="caption">服务名称:</Typography>
              <Typography variant="body2">{status.service_name}</Typography>
            </Grid>
          </Grid>

          {status.features && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
                可用功能:
              </Typography>
              <Box sx={{ ml: 1 }}>
                <FeatureStatus 
                  featureName="食谱生成" 
                  available={status.features.recipe_generation} 
                />
                <FeatureStatus 
                  featureName="食谱增强" 
                  available={status.features.recipe_enhancement} 
                />
                <FeatureStatus 
                  featureName="营养分析" 
                  available={status.features.nutrition_analysis} 
                />
                <FeatureStatus 
                  featureName="食材建议" 
                  available={status.features.ingredient_suggestion} 
                />
              </Box>
            </Box>
          )}

          {status.message && (
            <Alert severity="info" variant="outlined" size="small" sx={{ mt: 2 }}>
              <Typography variant="caption">{status.message}</Typography>
            </Alert>
          )}
        </Box>
      )}
    </Box>
  );
};

export default AIServiceStatus;