from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
from typing import Optional
import shutil
from confbadger import createBadge, read_data_file

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories if they don't exist
os.makedirs("badges", exist_ok=True)
os.makedirs("codes", exist_ok=True)
os.makedirs("temp", exist_ok=True)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Save the uploaded file temporarily
    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Read the CSV to validate it
        df = read_data_file(temp_file_path)
        required_columns = ["Order number", "First Name", "Last Name", "Email", "Company", "Title", "Ticket title"]
        
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail="CSV must contain all required columns")
        
        # Move the file to the main directory
        shutil.move(temp_file_path, "data.csv")
        
        # Generate badges
        createBadge()
        
        return {"message": "Badges generated successfully"}
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search-attendees")
async def search_attendees(
    name: Optional[str] = None,
    title: Optional[str] = None,
    company: Optional[str] = None,
    ticket_type: Optional[str] = None
):
    try:
        df = read_data_file("data.csv")
        # Apply filters
        if name:
            # Convert name to lowercase for case-insensitive search
            name = name.lower()
            # Create a mask for first name or last name containing the search term
            name_mask = (
                df["First Name"].str.lower().str.contains(name, na=False) |
                df["Last Name"].str.lower().str.contains(name, na=False)
            )
            df = df[name_mask]
            
        if title:
            df = df[df["Title"].str.contains(title, case=False, na=False)]
        if company:
            df = df[df["Company"].str.contains(company, case=False, na=False)]
        if ticket_type:
            df = df[df["Ticket title"].str.contains(ticket_type, case=False, na=False)]
        
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/badge/{filename}")
async def get_badge(filename: str):
    badge_path = f"badges/{filename}"
    if not os.path.exists(badge_path):
        raise HTTPException(status_code=404, detail="Badge not found")
    return FileResponse(badge_path)

@app.get("/list-badges")
async def list_badges():
    try:
        badges = os.listdir("badges")
        return {"badges": badges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 