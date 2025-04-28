from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
from typing import Optional
import shutil
from confbadger import createBadge, read_data_file, get_data_from_ticket_numbers
import logging
import glob

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

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

@app.on_event("startup")
async def clean_temp_folder():
    for file_path in glob.glob("temp/*.csv"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    logger.info(f"Received file upload: {file.filename}")
    
    # Save the uploaded file temporarily
    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    logger.info(f"Saved uploaded file to {temp_file_path}")
    
    try:
        # Read the CSV to validate it
        df = read_data_file(temp_file_path)
        required_columns = ["Ticket number", "First Name", "Last Name", "Email", "Company", "Title", "Ticket title"]
        
        logger.info(f"CSV columns: {', '.join(df.columns)}")
        
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            error_msg = f"CSV missing required columns: {', '.join(missing)}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Move the file to the main directory
        shutil.move(temp_file_path, "data.csv")
        logger.info("Moved temp file to data.csv")
        
        # Generate badges
        logger.info("Calling createBadge with save_path='codes'")
        try:
            badge_count = createBadge(save_path="codes")
            logger.info(f"createBadge returned: {badge_count} badges created")
        except Exception as e:
            logger.error(f"Error using createBadge with save_path='codes': {str(e)}")
            logger.info("Trying with default parameters...")
            try:
                badge_count = createBadge()
                logger.info(f"Success with default parameters: {badge_count} badges created")
            except Exception as e2:
                logger.error(f"Error using createBadge with default parameters: {str(e2)}")
                # As a last resort, try running the script directly
                logger.info("Trying with command line execution...")
                try:
                    os.system("python3 confbadger.py --data data.csv")
                    logger.info("Command line execution completed")
                    badge_count = len(os.listdir("badges"))
                except Exception as e3:
                    logger.error(f"Command line execution failed: {str(e3)}")
                    raise HTTPException(status_code=500, detail=f"Failed to generate badges: {str(e)} -> {str(e2)} -> {str(e3)}")
        
        # Check if badges were created
        badge_count = len(os.listdir("badges"))
        logger.info(f"Badge generation complete. {badge_count} badges in badges/")
        code_count = len(os.listdir("codes"))
        logger.info(f"QR code generation complete. {code_count} QR codes in codes/")
        
        return {"message": f"Badges generated successfully. {badge_count} badges created."}
    except Exception as e:
        logger.error(f"Error during badge generation: {str(e)}")
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
        
        ret = df.to_dict(orient="records")
        logger.debug(f"Search ret: {ret}")
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

@app.post("/upload-results-hash")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Save the uploaded file temporarily
    temp_file_path = f"temp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    shutil.move(temp_file_path, "post-scan-ticket-numbers.csv")
    df = get_data_from_ticket_numbers()
    os.remove("post-scan-ticket-numbers.csv")
    return {"participantdata": df.to_dict(orient="records")}

@app.get("/list-directories")
async def list_directories():
    try:
        badges_files = os.listdir("badges")
        codes_files = os.listdir("codes")
        files_in_root = os.listdir(".")
        return {
            "badges": badges_files,
            "codes": codes_files,
            "root_csv_files": [f for f in files_in_root if f.endswith('.csv')],
            "badge_count": len(badges_files),
            "code_count": len(codes_files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 