const dotenv = require('dotenv');

// 加载环境变量
dotenv.config();

module.exports = {
  // 主数据库连接配置
  primary: {
    url: process.env.DATABASE_URL,
    options: {
      // 连接池配置
      pool: {
        max: 20,
        min: 2,
        acquire: 30000,
        idle: 10000
      },
      // 其他连接选项
      dialectOptions: {
        ssl: process.env.NODE_ENV === 'production' ? {
          require: true,
          rejectUnauthorized: false
        } : false
      },
      // 启用详细日志
      logging: process.env.NODE_ENV === 'development'
    }
  },

  // 连接池配置（用于PgBouncer）
  pgbouncer: {
    url: process.env.PGBOUNCER_URL || 'postgresql://app_user:app_password@localhost:6432/recipe_system',
    enabled: process.env.USE_PGBOUNCER === 'true'
  },

  // 获取当前应该使用的数据库连接
  getConnectionConfig: function() {
    return this.pgbouncer.enabled ? this.pgbouncer : this.primary;
  },

  // 备份配置
  backup: {
    directory: process.env.BACKUP_DIR || 'd:/Homework/LLM/Final_assignment/Vers_4/backups',
    retentionDays: 30,
    cron: '0 2 * * *' // 每天凌晨2点执行备份
  }
};