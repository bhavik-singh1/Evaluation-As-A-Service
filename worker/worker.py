import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
def process_jobs():
    pending_jobs = supabase.table("eval_jobs").select("*").eq("status", "pending").execute()
    for job in pending_jobs.data:
        print(f"Processing job {job['id']} ...")

        # Simulate evaluation logic (placeholder)
        result_data = {"score": 95, "remarks": "Looks good!"}

        supabase.table("eval_jobs").update({
            "status": "completed",
            "result": result_data
        }).eq("id", job["id"]).execute()

        print(f"Job {job['id']} done ✅")

if __name__ == "__main__":
    process_jobs()
