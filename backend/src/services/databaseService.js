const { PrismaClient } = require('@prisma/client');
const databaseConfig = require('../config/database');

// 创建Prisma客户端实例
let prismaClient;

/**
 * 初始化数据库连接
 * @returns {Promise<PrismaClient>} Prisma客户端实例
 */
const initializeDatabase = async () => {
  try {
    // 获取连接配置
    const connectionConfig = databaseConfig.getConnectionConfig();
    
    // 创建Prisma客户端
    prismaClient = new PrismaClient({
      datasources: {
        db: {
          url: connectionConfig.url
        }
      },
      log: databaseConfig.primary.options.logging ? ['query', 'info', 'warn', 'error'] : ['error']
    });

    // 测试连接
    await prismaClient.$connect();
    console.log('数据库连接成功');
    
    return prismaClient;
  } catch (error) {
    console.error('数据库连接失败:', error.message);
    throw error;
  }
};

/**
 * 获取数据库客户端实例
 * @returns {PrismaClient} Prisma客户端实例
 */
const getDatabaseClient = () => {
  if (!prismaClient) {
    throw new Error('数据库客户端尚未初始化');
  }
  return prismaClient;
};

/**
 * 关闭数据库连接
 */
const closeDatabaseConnection = async () => {
  if (prismaClient) {
    await prismaClient.$disconnect();
    console.log('数据库连接已关闭');
  }
};

/**
 * 执行数据库事务
 * @param {Function} fn 事务回调函数
 * @returns {Promise<any>} 事务执行结果
 */
const executeTransaction = async (fn) => {
  const client = getDatabaseClient();
  return client.$transaction(fn);
};

module.exports = {
  initializeDatabase,
  getDatabaseClient,
  closeDatabaseConnection,
  executeTransaction
};