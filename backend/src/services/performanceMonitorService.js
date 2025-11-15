const { getDatabaseClient } = require('./databaseService');

/**
 * 数据库性能监控服务
 */
class PerformanceMonitorService {
  constructor() {
    this.prisma = null;
  }

  /**
   * 初始化监控服务
   */
  async initialize() {
    this.prisma = getDatabaseClient();
    console.log('数据库性能监控服务已初始化');
  }

  /**
   * 获取慢查询列表
   * @param {number} limit 返回的最大记录数
   * @returns {Promise<Array>} 慢查询列表
   */
  async getSlowQueries(limit = 10) {
    try {
      // 使用raw SQL查询慢查询统计信息
      const slowQueries = await this.prisma.$queryRaw`
        SELECT 
          query,
          calls,
          total_time,
          mean_time,
          rows
        FROM pg_stat_statements
        ORDER BY mean_time DESC
        LIMIT ${limit}
      `;
      
      return slowQueries;
    } catch (error) {
      console.error('获取慢查询列表失败:', error.message);
      return [];
    }
  }

  /**
   * 获取数据库大小信息
   * @returns {Promise<Object>} 数据库大小信息
   */
  async getDatabaseSize() {
    try {
      const result = await this.prisma.$queryRaw`
        SELECT 
          pg_size_pretty(pg_database_size('recipe_system')) AS database_size,
          pg_size_pretty(pg_total_relation_size('users')) AS users_table_size,
          pg_size_pretty(pg_total_relation_size('recipes')) AS recipes_table_size,
          pg_size_pretty(pg_total_relation_size('ingredients')) AS ingredients_table_size
      `;
      
      return result[0];
    } catch (error) {
      console.error('获取数据库大小失败:', error.message);
      return null;
    }
  }

  /**
   * 获取连接信息
   * @returns {Promise<Array>} 数据库连接信息
   */
  async getConnectionInfo() {
    try {
      const connections = await this.prisma.$queryRaw`
        SELECT 
          datname,
          usename,
          application_name,
          client_addr,
          state,
          query_start,
          now() - query_start AS duration,
          query
        FROM pg_stat_activity
        WHERE datname = 'recipe_system'
      `;
      
      return connections;
    } catch (error) {
      console.error('获取连接信息失败:', error.message);
      return [];
    }
  }

  /**
   * 获取索引使用情况
   * @returns {Promise<Array>} 索引使用情况
   */
  async getIndexUsage() {
    try {
      const indexUsage = await this.prisma.$queryRaw`
        SELECT
          schemaname,
          relname AS table_name,
          indexrelname AS index_name,
          idx_scan AS index_scans,
          idx_tup_read AS tuples_read,
          idx_tup_fetch AS tuples_fetched
        FROM pg_stat_user_indexes
        JOIN pg_index USING (indexrelid)
        WHERE schemaname = 'public'
        ORDER BY idx_scan DESC
      `;
      
      return indexUsage;
    } catch (error) {
      console.error('获取索引使用情况失败:', error.message);
      return [];
    }
  }

  /**
   * 检查数据库健康状态
   * @returns {Promise<Object>} 健康状态信息
   */
  async checkHealth() {
    try {
      // 执行简单的查询来验证数据库连接
      await this.prisma.$queryRaw`SELECT 1`;
      
      // 获取数据库活动和大小信息
      const [connections, size] = await Promise.all([
        this.getConnectionInfo(),
        this.getDatabaseSize()
      ]);
      
      return {
        status: 'healthy',
        connections: connections.length,
        databaseSize: size.database_size,
        timestamp: new Date()
      };
    } catch (error) {
      console.error('数据库健康检查失败:', error.message);
      return {
        status: 'unhealthy',
        error: error.message,
        timestamp: new Date()
      };
    }
  }
}

module.exports = new PerformanceMonitorService();