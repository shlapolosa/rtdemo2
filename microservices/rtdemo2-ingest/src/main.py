"""Realtime INGEST (generated, RT-2). POST /ingest -> handlers.to_message ->
produce to the declared PRODUCE_* topic. Transport via realtime-transport."""
import os
from realtime_transport import create_realtime_ingest_app
from src.handlers import to_message

SERVICE_NAME = os.getenv("WEBSERVICE_NAME", os.getenv("REALTIME_PLATFORM_NAME", "realtime-ingest"))

app = create_realtime_ingest_app(
    service_name=SERVICE_NAME,
    to_message=to_message,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
