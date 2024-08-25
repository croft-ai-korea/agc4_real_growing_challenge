module.exports = {
    apps: [
      {
        name: "per_5min",
        script: "python3",
        args: "aaaa/per_5min.py",
        cron_restart: "*/5 * * * *", // Run every 5  minutes
        restart_delay : 60000,
        watch: true
      },
      {
        name: "per_day",
        script: "python3",
        args: "aaaa/per_day.py",
        cron_restart: "10 0 * * *", // Run every day
        restart_delay : 60000,
        watch: true
      }
    ]
  };