# Pigilan: A Progressive Web App for Early Detection and Warning of African Swine Fever

## Introduction

African Swine Fever (ASF) is a highly contagious disease that causes severe losses in the swine industry. Early detection is important to prevent the rapid spread of the virus, especially among small-scale pig farmers who may lack access to immediate veterinary assistance. However, many farmers find it difficult to identify early symptoms of ASF and determine the proper actions to take.

PIGilan is a web-based system designed to assist farmers in identifying possible signs of ASF through symptom selection and image analysis. The system provides risk assessments and guidance on isolation, first aid, and when to consult veterinary authorities. By integrating technology into livestock management, the application aims to promote early detection, improve biosecurity practices, and help reduce the spread of ASF.

## Problem Statement

African Swine Fever (ASF) is a highly contagious viral disease that affects pigs and causes severe economic losses to farmers and the livestock industry. Since there is no cure or vaccine for this disease, early detection and immediate containment are essential to prevent outbreaks and minimize damage. Unfortunately, many small-scale and backyard pig farmers lack sufficient knowledge about the early symptoms of ASF. They often struggle to differentiate ASF from other common swine diseases and may delay reporting due to uncertainty or limited access to veterinary services.

As a result, infected animals are isolated late, allowing the disease to spread rapidly within farms and nearby areas. This can lead to large-scale culling, serious financial losses, and threats to food security and the local economy. Therefore, there is a need for a digital, accessible, and farmer-friendly system that can assist in early detection, risk assessment, structured reporting, and biosecurity guidance to help reduce the spread of African Swine Fever.

## General Objectives

- Develop a system that assists pig farmers in identifying early warning signs of African Swine Fever (ASF).
- Generate a reliable risk assessment system based on reported symptoms and health data.
- Promote timely preventive and containment actions to reduce the spread of ASF.
- Strengthen farm biosecurity practices through guided protocols and monitoring tools.
- Generate alerts from nearby possible cases of ASF.
- Use machine learning-based image recognition to analyze photos of pigs and identify possible visual symptoms related to ASF.

## Features

- ASF risk assessment
- Early warning alerts
- Biosecurity checklist
- Case report sharing
- Offline access
- ASF image detection

## Project Checklist

- [x] ASF risk assessment
- [x] Early warning alerts
- [x] Biosecurity checklist
- [x] Case report sharing
- [x] Offline access
- [x] ASF image detection
- [x] Streamlit frontend
- [x] Python backend
- [x] SQLite database
- [x] Teachable Machine integration

## Tech Stack

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- Machine Learning: Teachable Machine
- Deployment: Streamlit Cloud or local server

## How To Run

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

Run the Streamlit app:

```powershell
streamlit run app.py
```

The app usually opens at:

```text
http://localhost:8501
```

## Default Admin Account

- Username: `admin`
- Password: `admin123`

Change the default admin account before real deployment.
