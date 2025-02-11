import os


class RunwareSettings:
    RUNWARE_API_KEY = os.getenv("RUNWARE_API_KEY")


class RabbitMQSettings:
    AMQP_URL = os.getenv("AMQP_URL")
