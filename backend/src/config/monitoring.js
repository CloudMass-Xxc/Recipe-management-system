/**
 * 数据库性能监控配置
 */
module.exports = {
  // 慢查询监控配置
  slowQuery: {
    // 慢查询阈值（毫秒）
    thresholdMs: 1000,
    // 监控间隔（秒）
    checkInterval: 300,
    // 保存历史记录天数
    historyDays: 7
  },
  
  // 连接池监控配置
  connectionPool: {
    // 最大连接数警告阈值（百分比）
    maxConnectionsWarningThreshold: 80,
    // 空闲连接最小数量
    minIdleConnections: 2,
    // 监控间隔（秒）
    checkInterval: 60
  },
  
  // 数据库大小监控
  databaseSize: {
    // 监控间隔（小时）
    checkInterval: 24,
    // 增长告警阈值（百分比/天）
    growthWarningThreshold: 10
  },
  
  // 索引监控
  indexMonitoring: {
    // 未使用索引检查间隔（天）
    unusedIndexCheckInterval: 7,
    // 自动收集统计信息（布尔值）
    autoCollectStats: true
  },
  
  // 告警配置
  alerts: {
    // 邮件告警配置
    email: {
      enabled: false,
      recipients: ['admin@example.com'],
      sender: 'monitoring@example.com'
    },
    // 系统日志告警
    systemLog: {
      enabled: true,
      logLevel: 'warn'
    },
    // 告警阈值
    thresholds: {
      // 连续失败次数
      consecutiveFailures: 3,
      // 恢复通知
      sendRecoveryNotification: true
    }
  },
  
  // 监控日志配置
  logs: {
    // 日志级别
    level: 'info',
    // 日志文件路径
    filePath: 'logs/monitoring.log',
    // 日志轮转配置
    rotation: {
      size: '100m',
      files: 10
    }
  }
};