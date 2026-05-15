"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team-based basketball training and friendly games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu"]
    },
    "Soccer Camp": {
        "description": "Soccer drills, teamwork practice, and weekend matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 24,
        "participants": ["ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Draw, paint, and explore creative art projects together",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["sophia@mergington.edu"]
    },
    "Drama Workshop": {
        "description": "Acting exercises, stagecraft, and short performance practice",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mason@mergington.edu"]
    },
    "Debate Society": {
        "description": "Prepare arguments and compete in structured debate rounds",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["sophia@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Build science projects and practice STEM problem solving",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu"]
    }
}



@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    #Validate email format (simple check)
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")     

    # Prevent duplicate signups
    if email in activity.get("participants", []):
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Enforce max participants
    max_participants = activity.get("max_participants")
    if max_participants is not None and len(activity.get("participants", [])) >= max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity.setdefault("participants", []).append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity.get("participants", []):
        raise HTTPException(status_code=404, detail="Participant not found for this activity")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
