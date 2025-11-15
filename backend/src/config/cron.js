const backupService = require('../services/backupService');

/**
 * 定时任务配置
 */
module.exports = {
  // 任务列表
  jobs: [
    {
      // 数据库备份任务
      name: 'databaseBackup',
      schedule: '0 2 * * *', // 每天凌晨2点执行
      task: async () => {
        try {
          console.log('执行数据库备份任务');
          const backupFile = await backupService.createBackup();
          console.log(`数据库备份任务完成，备份文件: ${backupFile}`);
        } catch (error) {
          console.error('数据库备份任务失败:', error.message);
        }
      }
    },
    {
      // 数据库优化任务
      name: 'databaseMaintenance',
      schedule: '0 3 * * 0', // 每周日凌晨3点执行
      task: async () => {
        try {
          console.log('执行数据库维护任务');
          // 这里可以添加VACUUM和ANALYZE等维护操作
          // 注意：实际执行需要使用数据库连接执行SQL命令
          console.log('数据库维护任务完成');
        } catch (error) {
          console.error('数据库维护任务失败:', error.message);
        }
      }
    }
  ],
  
  // 任务管理函数
  start: async (cron) => {
    // 启动所有任务
    const scheduledJobs = [];
    
    for (const job of module.exports.jobs) {
      console.log(`启动定时任务: ${job.name} (${job.schedule})`);
      const scheduledJob = cron.schedule(job.schedule, job.task);
      scheduledJobs.push({ name: job.name, job: scheduledJob });
    }
    
    return scheduledJobs;
  },
  
  stop: async (jobs) => {
    // 停止所有任务
    for (const { name, job } of jobs) {
      console.log(`停止定时任务: ${name}`);
      job.stop();
    }
  }
};