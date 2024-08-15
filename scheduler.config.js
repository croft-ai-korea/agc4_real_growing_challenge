module.exports = {
    apps: [
      {
        name: "stragety_day",
        script: "python3",
        args: "strategy_day_test.py",
        cron_restart: "0 0 * * *", // Run at midnight
        restart_delay : 60000
      },
      {
        name: "stragety_5min",
        script: "python3",
        args: "strategy_5min_test.py",
        cron_restart: "*/1 * * * *", // Run every 1 minutes
        restart_delay : 60000
      }
    ]
  };