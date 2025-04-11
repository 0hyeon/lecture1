from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import json
from kafka import KafkaProducer
from datetime import datetime
import logging

# FastAPI 앱 설정
app = FastAPI()

# Kafka 프로듀서 설정 (Kafka 브로커 주소는 외부 IP와 포트를 사용)
producer = KafkaProducer(
    bootstrap_servers="34.118.235.52:9092",  # Kafka 외부 IP와 포트
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


# Pydantic 모델을 사용해 입력을 받을 데이터 정의
class Input(BaseModel):
    id: str
    status: str
    product: str
    price: int
    discount_price: int
    discount_rate: int
    category: str


# Kafka에 메시지를 보내는 함수
def process_message_to_kafka(message: dict):
    # 카프카 토픽 'category-match-out'에 메시지를 전송
    producer.send("category-match-out", value=message)
    logging.info(f"Message sent to Kafka topic 'category-match-out': {message}")


@app.post("/predict")
async def predict(input: Input, background_tasks: BackgroundTasks):
    request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Kafka에 보낼 메시지 포맷
    message = {
        "id": input.id,
        "status": input.status,
        "product": input.product,
        "price": input.price,
        "discount_price": input.discount_price,
        "discount_rate": input.discount_rate,
        "category": input.category,
        "request_time": request_time,
    }

    # 백그라운드 작업으로 Kafka에 메시지 보내기
    background_tasks.add_task(process_message_to_kafka, message)

    # 즉시 응답을 반환
    return {"status": "Message received and processing in the background"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
