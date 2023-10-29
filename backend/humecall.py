#!/venv/bin/python
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

client = HumeBatchClient("GB5GR8utyBkDmLHy5Kh7mtAGGebtMK5R9nDVhn7p5u7FMcT2")
urls = ["https://tmpfiles.org/dl/2979437/untitled.mp3"]
configs = [ProsodyConfig(identify_speakers = True)]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")

df = pd.read_json('/predicitions.json')
print(df)