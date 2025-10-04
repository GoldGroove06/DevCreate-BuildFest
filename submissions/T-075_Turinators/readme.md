
# Vaahan-Saarthi 🚗🛣️(Open Innovation Challenge)

## 🏷 Team Details
- **Team Name:** Turinators
- **Team ID:** T-075

### 👥 Members & Roles
- **Gurneet Singh** – Project Lead / ML Engineer
- **Geetansh Gatumn** – ML Engineer (YOLO Model Training) /Presenter
- **Manpreet Singh** –  ML Engineer (YOLO Model Training)  
- **Arshpreet Singh** – Frontend Developer (Visualization & UI) 

---

## 📌 Problem Statement
### India faces a severe challenge due to pothole-ridden roads. According to reports, **over 11,000 road accident deaths are linked to potholes**. Despite technological advances in automobiles, **there is no standard built-in solution in vehicles to detect and alert drivers about potholes**.  

#### Solution
Our project addresses this issue by leveraging **Computer Vision (YOLO-based object detection)** to automatically detect and **mark potholes from real-time road footage**. The system not only identifies potholes but also makes **driving suggestions such as slowing down or steering assistance**.

Looking ahead, this solution can be integrated with **ADAS (Advanced Driver Assistance Systems)** in vehicles to give drivers a proactive advantage, especially in India where road infrastructure challenges are significant. This approach enables **safer driving, accident prevention, and proactive road maintenance**..  

---

## 🛠 Tech Stack
- **Machine Learning:** YOLOv8 (custom trained model for pothole detection)  
- **Backend:** Flask (serving detection results, for visualization and reporting)  
- **Frontend:** React / Vite    
- **Other Tools:** OpenCV, Numpy  

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
#### backend
```bash
cd backend 
pip install -r requirements.txt
flask run
```
#### frontend
```bash
cd frontend
npm install
npm run dev
