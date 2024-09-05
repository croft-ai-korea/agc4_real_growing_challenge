module.exports = {
    apps: [
      {
        name: "per_5min",
        script: "python3",
        args: "aaaa/per_5min.py",
        cron_restart: "*/5 * * * *", // Run every 5 minutes
        restart_delay : 60000,
        // watch: true,
        max_restarts: 1, // 최대 재시도 횟수 1번
        min_uptime: "180s", // 최소 3분 동안 실행되어야 함
        exec_mode: "fork", // 포크 모드로 실행
      },
      {
        name: "per_day",
        script: "python3",
        args: "aaaa/per_day.py",
        cron_restart: "0 1 * * *", // Run every day at 01:00
        restart_delay : 60000,
        timezone: "Europe/Amsterdam", // 네덜란드 시간대 기준
        // watch: true,
        max_restarts: 5, // 최대 재시도 횟수 5번
        min_uptime: "180s", // 최소 3분 동안 실행되어야 함
        exec_mode: "fork", // 포크 모드로 실행
      },
      {
        name: "per_15min",
        script: "python3",
        args: "aaaa/per_15min.py",
        cron_restart: "*/15 * * * *", // Run every day at 15min
        restart_delay : 60000, 
        // watch: true
        max_restarts: 2, // 최대 재시도 횟수 5번
        min_uptime: "180s", // 최소 3분 동안 실행되어야 함
        exec_mode: "fork", // 포크 모드로 실행
      }
    ]
  };