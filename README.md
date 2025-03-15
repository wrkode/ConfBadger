# Conference Badge Generator

A web application for generating and managing conference badges from CSV data. The application allows you to upload attendee data, generate badges with QR codes, and search through attendees.

## Features

- Upload CSV files with attendee information
- Generate badges with QR codes containing attendee details
- Search attendees by name, title, company, or ticket type
- Preview and download individual badges
- Real-time search with instant results
- Modern, responsive user interface

## Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- npm (Node Package Manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ConfBadger
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the FastAPI backend (from the root directory):
```bash
python app.py
```
The backend will be available at http://localhost:8000

2. Start the React frontend (from the frontend directory):
```bash
cd frontend
npm start
```
The frontend will be available at http://localhost:3000

## CSV File Format

The application expects a CSV file with the following columns:
- Order #
- First Name
- Last Name
- Email
- Phone Number
- Country
- Country Code
- Job Title
- Company
- Discount

Example CSV format:
```csv
Order #,First Name,Last Name,Email,Phone Number,Country,Country Code,Job Title,Company,Discount
1,John,Doe,john@example.com,+1234567890,Netherlands,NL,Software Engineer,Example Corp,100.00% - KCDAMS23_ORGANIZERS_42
```

## Usage

1. **Upload CSV File**
   - Click the "Upload CSV File" button
   - Select your CSV file with attendee information
   - The system will validate the file and generate badges

2. **Search Attendees**
   - Use the search fields to filter attendees by:
     - Name (searches in both first and last name)
     - Title
     - Company
     - Ticket Type
   - Results update automatically as you type
   - Clear individual fields using the X button
   - Reset all filters using the "Clear Search" button

3. **Preview and Download Badges**
   - Each attendee card shows basic information
   - Use the "Preview Badge" button to view the badge in a new tab
   - Use the "Download" button to download the badge

## Project Structure

```
ConfBadger/
├── app.py                 # FastAPI backend
├── confbadger.py          # Badge generation logic
├── requirements.txt       # Python dependencies
├── data.csv              # Sample CSV file
├── KCDAMS2023_Badge_Template.png  # Badge template
├── frontend/             # React frontend
│   ├── package.json
│   ├── public/
│   └── src/
├── badges/              # Generated badges
├── codes/               # Generated QR codes
├── fonts/               # Font files
└── flags/               # Country flag images
```

## Development

- Backend: FastAPI (Python)
- Frontend: React with Material-UI
- Badge Generation: PIL (Python Imaging Library)
- QR Code Generation: PyQRCode

## License

This project is licensed under the MIT License - see the LICENSE file for details.