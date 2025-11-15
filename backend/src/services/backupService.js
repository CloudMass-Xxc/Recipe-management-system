const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const databaseConfig = require('../config/database');

// 转换为Promise
const execPromise = util.promisify(exec);

/**
 * 创建数据库备份
 * @returns {Promise<string>} 备份文件路径
 */
const createBackup = async () => {
  try {
    const backupDir = databaseConfig.backup.directory;
    
    // 创建备份目录（如果不存在）
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }
    
    // 生成时间戳
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFile = path.join(backupDir, `recipe_system_backup_${timestamp}.sql`);
    
    // 构建pg_dump命令
    const command = `pg_dump -U app_user -d recipe_system -f "${backupFile}"`;
    
    console.log(`开始创建数据库备份: ${backupFile}`);
    await execPromise(command);
    
    // 压缩备份文件
    const compressedFile = backupFile + '.gz';
    await execPromise(`gzip -c "${backupFile}" > "${compressedFile}"`);
    
    // 删除未压缩的文件
    fs.unlinkSync(backupFile);
    
    console.log(`备份完成: ${compressedFile}`);
    
    // 清理旧备份
    await cleanupOldBackups();
    
    return compressedFile;
  } catch (error) {
    console.error('创建备份失败:', error.message);
    throw error;
  }
};

/**
 * 从备份恢复数据库
 * @param {string} backupFilePath 备份文件路径
 * @returns {Promise<void>}
 */
const restoreFromBackup = async (backupFilePath) => {
  try {
    // 检查备份文件是否存在
    if (!fs.existsSync(backupFilePath)) {
      throw new Error(`备份文件不存在: ${backupFilePath}`);
    }
    
    console.log(`开始从备份恢复: ${backupFilePath}`);
    
    // 构建恢复命令
    let command;
    if (backupFilePath.endsWith('.gz')) {
      // 对于压缩文件
      command = `gunzip -c "${backupFilePath}" | psql -U app_user -d recipe_system`;
    } else {
      // 对于未压缩文件
      command = `psql -U app_user -d recipe_system -f "${backupFilePath}"`;
    }
    
    await execPromise(command);
    console.log('数据库恢复完成');
  } catch (error) {
    console.error('数据库恢复失败:', error.message);
    throw error;
  }
};

/**
 * 清理旧的备份文件
 */
const cleanupOldBackups = async () => {
  try {
    const backupDir = databaseConfig.backup.directory;
    const retentionDays = databaseConfig.backup.retentionDays;
    
    // 检查目录是否存在
    if (!fs.existsSync(backupDir)) {
      return;
    }
    
    const files = fs.readdirSync(backupDir);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retentionDays);
    
    files.forEach(file => {
      if (file.startsWith('recipe_system_backup_') && file.endsWith('.sql.gz')) {
        const filePath = path.join(backupDir, file);
        const stats = fs.statSync(filePath);
        
        if (stats.birthtime < cutoffDate) {
          console.log(`删除过期备份: ${file}`);
          fs.unlinkSync(filePath);
        }
      }
    });
  } catch (error) {
    console.error('清理旧备份失败:', error.message);
  }
};

/**
 * 获取备份列表
 * @returns {Promise<Array>} 备份文件列表
 */
const listBackups = async () => {
  try {
    const backupDir = databaseConfig.backup.directory;
    
    // 检查目录是否存在
    if (!fs.existsSync(backupDir)) {
      return [];
    }
    
    const files = fs.readdirSync(backupDir)
      .filter(file => file.startsWith('recipe_system_backup_') && file.endsWith('.sql.gz'))
      .map(file => {
        const filePath = path.join(backupDir, file);
        const stats = fs.statSync(filePath);
        return {
          name: file,
          path: filePath,
          size: stats.size,
          created: stats.birthtime
        };
      })
      .sort((a, b) => b.created - a.created); // 按创建时间倒序排序
    
    return files;
  } catch (error) {
    console.error('获取备份列表失败:', error.message);
    return [];
  }
};

module.exports = {
  createBackup,
  restoreFromBackup,
  cleanupOldBackups,
  listBackups
};