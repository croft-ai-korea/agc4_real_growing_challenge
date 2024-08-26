from datetime import datetime

def test_scheduled_function():
    # Your scheduled function here
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"strategy_5min function executed at {current_time}")

    print(datetime(2024,11,26) - datetime(2024,9,5))
if __name__ == "__main__":
    test_scheduled_function()