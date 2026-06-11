"""Realtime PROCESSOR (generated, RT-2). Consume declared CONSUME_* topics ->
handlers.transform -> produce to the declared PRODUCE_* topic. Transport via
realtime-transport."""
import os
from realtime_transport import create_realtime_processor_app
from src.handlers import transform

SERVICE_NAME = os.getenv("WEBSERVICE_NAME", os.getenv("REALTIME_PLATFORM_NAME", "realtime-processor"))

app = create_realtime_processor_app(
    service_name=SERVICE_NAME,
    transform=transform,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
