#!/venv/bin/python
from hume import HumeBatchClient
from hume.models.config import FaceConfig

client = HumeBatchClient("GB5GR8utyBkDmLHy5Kh7mtAGGebtMK5R9nDVhn7p5u7FMcT2i")
urls = ["https://iep.utm.edu/wp-content/media/hume-bust.jpg"]
config = FaceConfig()
job = client.submit_job(urls, [config])

status = job.get_status()
print(f"Job status: {status}")

details = job.get_details()
run_time_ms = details.get_run_time_ms()
print(f"Job ran for {run_time_ms} milliseconds")