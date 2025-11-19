module.exports = {
    apps: [
        {
            // 应用名称
            name: 'anan-chatbox-api',
            // Python 脚本路径
            script: 'api.py',
            // 使用 python3 作为解释器
            interpreter: 'python3',
            // 工作目录 - 请根据实际部署路径修改
            cwd: './',
            // 实例数量
            instances: 1,
            // 执行模式：fork（单实例）或 cluster（多实例）
            exec_mode: 'fork',
            // 自动重启
            autorestart: true,
            // 文件变化监控（生产环境建议设为 false）
            watch: false,
            // 内存超过 500M 时自动重启
            max_memory_restart: '500M',
            // 日志文件路径（PM2 会自动创建 logs 目录）
            error_file: './logs/err.log',
            out_file: './logs/out.log',
            // 日志日期格式
            log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
            // 合并日志
            merge_logs: true,
            // 环境变量
            env: {
                NODE_ENV: 'production',
                // 启用 Python 无缓冲输出，确保日志实时输出
                PYTHONUNBUFFERED: '1'
            },
            // 自动重启配置
            min_uptime: '10s',        // 最短运行时间，少于此时长的重启视为异常
            max_restarts: 10,          // 最大重启次数
            restart_delay: 4000,       // 重启延迟（毫秒）
        }
    ]
};

