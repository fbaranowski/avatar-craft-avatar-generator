import logging

from fastapi import FastAPI

from core.rabbitmq import RabbitMQClient

app = FastAPI()

rabbitmq_client = RabbitMQClient()


@app.on_event("startup")
async def startup_event():
    logging.info("RabbitMQ consumer starting...")
    await rabbitmq_client.start_consuming()
    logging.info("RabbitMQ consumer started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down RabbitMQ consumer...")
    await rabbitmq_client.close()
    logging.info("RabbitMQ consumer connection closed")


@app.get("/")
async def root():
    return {"message": "Avatar generator app is running..."}
