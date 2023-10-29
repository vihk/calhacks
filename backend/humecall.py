#!/venv/bin/python
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

client = HumeBatchClient("GB5GR8utyBkDmLHy5Kh7mtAGGebtMK5R9nDVhn7p5u7FMcT2")
urls = ["https://storage.googleapis.com/hume-test-data/video/armisen-clip.mp4"]
configs = [ProsodyConfig(identify_speakers = True)]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")
