module.exports = {
    apps: [
      {
        name: "per_5min",
        script: "python3",
        args: "aaaa/per_5min.py",
        cron_restart: "*/5 * * * *", // Run every 5 minutes
        restart_delay : 60000,
        watch: true
      },
      {
        name: "per_day",
        script: "python3",
        args: "aaaa/per_day.py",
        cron_restart: "30 0 * * *", // Run every day at 00:30
        restart_delay : 60000,
        watch: true
      },
      {
        name: "per_15min",
        script: "python3",
        args: "aaaa/per_15min.py",
        cron_restart: "*/15 * * * *", // Run every day at 15min
        restart_delay : 60000,
        watch: true
      }
    ]
  };