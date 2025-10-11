import asyncio
import requests
from supabase import create_client
from realtime import AsyncRealtimeClient


# Supabase setup
SUPABASE_URL = "https://tyipioljdtxygsldixym.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR5aXBpb2xqZHR4eWdzbGRpeHltIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTgxMzAzMCwiZXhwIjoyMDc1Mzg5MDMwfQ.hLwyugKkchw4u6c7Qpl4dvHiQ-w6IhfmXGvuGS6wW_I"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# ------------------------------
# 2️⃣ Realtime client
# ------------------------------
REALTIME_URL = "wss://tyipioljdtxygsldixym.supabase.co/realtime/v1"
socket = AsyncRealtimeClient(REALTIME_URL, SUPABASE_KEY)

# ------------------------------
# 3️⃣ Evaluation logic
# ------------------------------
def evaluate(file_data, rubric_id):
    """Simple example: count CSV lines."""
    return {"lines": len(file_data.splitlines()), "rubric_id": rubric_id}

# ------------------------------
# 4️⃣ Async job processor
# ------------------------------
async def handle_job(payload):
    job = payload['record']
    job_id = job['id']
    file_url = job['file_url']
    rubric_id = job['rubric_id']

    print(f"[Worker] New job detected: {job_id}")

    try:
        # Fetch file
        response = requests.get(file_url)
        file_data = response.text

        # Evaluate
        result = evaluate(file_data, rubric_id)

        # Update job in DB
        await supabase.table('eval_jobs').update({
            "result": result,
            "status": "completed"
        }).eq("id", job_id).execute()

        print(f"[Worker] Job {job_id} completed successfully.")

    except Exception as e:
        # Mark job as failed
        await supabase.table('eval_jobs').update({
            "status": "failed"
        }).eq("id", job_id).execute()
        print(f"[Worker] Job {job_id} failed: {e}")

# ------------------------------
# 5️⃣ Sync wrapper for realtime callback
# ------------------------------
def handle_job_sync(payload):
    print("DEBUG PAYLOAD:", payload)  # <-- check structure
    print("DEBUG PAYLOAD RECORD:", payload.get('record'))  # <-- check structure

    # Schedule async job in event loop
    asyncio.create_task(handle_job(payload))

# ------------------------------
# 6️⃣ Subscribe to new jobs
# ------------------------------
async def subscribe_to_jobs():
    channel = socket.channel("eval_jobs_channel")

    # Register callback (sync wrapper)
    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="eval_jobs",
        callback=handle_job_sync
    )

    # Subscribe (await this)
    await channel.subscribe()
    print("[Worker] Listening for new evaluation jobs...")

    # Keep alive
    while True:
        await asyncio.sleep(10)

# ------------------------------
# 7️⃣ Run the worker
# ------------------------------
if __name__ == "__main__":
    asyncio.run(subscribe_to_jobs())
