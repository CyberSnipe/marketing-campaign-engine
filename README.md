# README.md

# Project Title
Marketing Campaign Engine

# Project Description
The Marketing Campaign Engine is a modular Python application that simulates a single business process: triggering a marketing campaign and calculating how much inventory should be restocked based on projected demand. Users enter product information, and the system generates a restock recommendation including quantity and total cost.

This project demonstrates multi‑module program design, JSON file handling, classes, functions, error handling, and automated testing.

# Purpose
This project was created as the Final Project for COP3045 – Programming II.  
It is designed to show mastery of core programming concepts through a clean, well‑structured, and realistic business workflow.

# How to Run

## 1. Clone the Repository
git clone https://github.com/<your-username>/marketing-campaign-engine.git
cd marketing-campaign-engine

## 2. Create and Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Run the Application
python main.py

# Dependencies
pytest

Everything else uses the Python Standard Library.

# Core Features
- Trigger Marketing Campaign  
- Demand Projection Logic  
- Restock Recommendation Output  
- JSON Persistence  
- Input Validation & Error Handling  
- Help / Documentation in CLI  

# Code Organization

marketing_campaign_project/
│
├── main.py
├── settings.cfg
│
├── api/
│     └── marketing_api.py
│
├── domain/
│     └── merch_item.py
│
├── services/
│     └── marketing_service.py
│
├── persistence/
│     ├── merch_repository.py
│     └── restock_repository.py
│
├── routing/
│     └── process_router.py
│
├── tests/
│     └── test_marketing_process.py
│
└── data/
      ├── merch_catalog.json
      └── restock_recommendations.json


# Testing
pytest

Tests cover:
- Core business logic  
- Edge cases  
- Error scenarios  
- JSON read/write behavior  

# Presentation Requirements
- 3–5 minute demo video  
- Code walkthrough  
- Architecture explanation  
- Challenges and solutions  
- Future improvement ideas  

# Future Improvements
- GUI interface  
- SQL backend  
- Batch processing  
- Data visualization  
- Integration with a full ERP system  

# Grading Rubric Alignment
Code Functionality – 30%  
Code Quality & Organization – 20%  
Concepts Coverage – 20%  
Documentation – 15%  
Creativity & Features – 10%  
Presentation – 5%  

# Author
Joseph Bevels
COP3045 – Python Programming  
University of North Florida

