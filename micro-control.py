import RPi.GPIO as GPIO
import time
import telebot


SENSOR_PIN = 15  # GPIO pin connected to the door sensor

THRESHOLD_SECONDS = 300  # 5 minutes


TELEGRAM_BOT_TOKEN = '[put your telegram key here]'


GPIO.setmode(GPIO.BCM)  # Initialized GPIO
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)  # Initialize Telegram


def send_notification():
    title = "Refrigerator Door is Open"
    message = "The refrigerator door has been left open for too long!"
    chat_id = 'ID' # Add your chat id

    
    bot.send_message(chat_id, f"{title}\n{message}") # Send the message to Telegram


try:
    door_open_time = None

    while True:
        door_state = GPIO.input(SENSOR_PIN)

        if door_state == GPIO.LOW:
            # The door is open
            if door_open_time is None:
                door_open_time = time.time()
            else:
                elapsed_time = time.time() - door_open_time
                if elapsed_time >= THRESHOLD_SECONDS:
                    send_notification()
                    door_open_time = None
        else:
            # The door is closed
            door_open_time = None

        time.sleep(1)  # Check the door state every 1 second

except KeyboardInterrupt:
    GPIO.cleanup() # break the execution of the program 
