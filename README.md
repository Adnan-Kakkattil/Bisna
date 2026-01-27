# 🎓EduStack
A modern, sleek College Management System built with **Flask** and **SQLAlchemy**, featuring a glassmorphism-inspired dark theme.

Bisna streamlines college administration by providing distinct portals for students, teachers, and administrators. It features a robust Role-Based Access Control (RBAC) system to ensure secure interactions and syllabus-centric resource management.

## ✨ Key Features

### 🎨 User Interface
- **Glassmorphism Design**: A premium, high-end aesthetic using blur and transparency effects.
- **Mobile First**: Fully responsive layout optimized for all device sizes.
- **Micro-interactions**: Smooth transitions and hover effects for an engaging experience.

### 🔐 Access Control
- **Multi-Role Portals**: Dedicated experiences for Super Admin, College Admin, Teacher, and Student.
- **Secure Sessions**: Powered by `Flask-Login` with encrypted password hashing.

### 📚 Modules
- **Syllabus Management**: Hierarchical structure from Courses down to individual Topics.
- **Resource Distribution**: Teachers can upload study materials (PDF, DOCX, Video, or URLs).
- **Verification Workflow**: Content can be reviewed and verified by teachers or admins before becoming public.

## 🎨 Core Aesthetic

EduStack utilizes a bespoke Neumorphic (Soft UI) design system, creating a tactile and immersive digital experience.

| Landing Page | Login Page |
| :---: | :---: |
| ![Landing Page](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_0_1769511425121.png) | ![Login Page](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_1_1769511425121.png) |

| Super Admin Dashboard | Admin Dashboard |
| :---: | :---: |
| ![Super Admin Dashboard](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_2_1769511425121.png) | ![Admin Dashboard](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_3_1769511425121.png) |

| Teacher Portal | Student Dashboard |
| :---: | :---: |
| ![Teacher Portal](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_4_1769511425121.png) | ![Student Dashboard](file:///C:/Users/LENOVO/.gemini/antigravity/brain/5ee8c34f-12e0-4df1-a5d9-a20c81ddd157/uploaded_media_1769511719893.png) |

## �🛠️ Tech Stack
- **Backend**: Python, Flask, Jinja2
- **Database**: SQLite (Dev), SQLAlchemy (ORM)
- **Frontend**: Vanilla JavaScript, CSS3 (Modern Flexbox/Grid)
- **File Delivery**: Cloudinary (CDN Support)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python Package Installer)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/c0zm3k/Bisna.git
   cd Bisna
   ```

2. **Set up Virtual Environment**
   ```powershell
   # Windows (PowerShell)
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration (.env)**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=dev-secret-key
   DATABASE_URL=sqlite:///site.db
   ```

5. **Initialize Database & Seed Data**
   ```bash
   python bin/setup_db.py
   python bin/seed_final_data.py
   ```

6. **Institutional Credentials**
   A complete, sorted list of access credentials for all roles and colleges is located in:
   `login_credentials.txt`

6. **Run the Application**
   ```bash
   python run.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## 👤 Test Credentials

The system is pre-seeded with multiple demo accounts. Use these for testing:

### 🌟 Super Admin
| Email | Password | Access Level |
| :--- | :--- | :--- |
| `superadmin@example.com` | `admin123` | Full System Control, College Management |

## 🏢 College Directory

The system is organized into multiple independent institutional nodes. Each college has a unique **College ID (CIDA)**.

| College Name | College ID | Slug |
| :--- | :--- | :--- |
| **Oxford Technical University** | `CIDA001` | `oxfor` |
| **Cambridge Science Academy** | `CIDA002` | `cambr` |
| **Stanford Institute of Excellence** | `CIDA003` | `stanf` |
| **MIT Global College** | `CIDA004` | `mitgl` |
| **Ethoz Business School** | `CIDA005` | `ethoz` |
| **Apex Engineering Institute** | `CIDA006` | `apexe` |

## 👤 User Directory & Credentials

The system is pre-seeded with **~666 total accounts** across all colleges.

### 🌟 Global Access
A complete list of credentials (Admin, Teacher, Student) for all colleges can be found in `login_credentials.txt`.

### 🎓 Institutional Access (Per College)
For any college listed above, use the following patterns (replace `[slug]` with the college slug):

| Role | Email Pattern | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@[slug].edu` | `password123` |
| **Teacher** | `teacher[1-10]@[slug].edu` | `password123` |
| **Student** | `student[teacher_idx]_[1-10]@[slug].edu` | `password123` |

> [!TIP]
> Each **Teacher** is seeded with **at least 3 resources** (PDFs, Docs, or URLs) associated with their specific college syllabus.

## 📂 Project Structure
```text
Bisna/
├── app/               # Flask Application & Core Logic
├── bin/               # Maintenance & Seeding Scripts
├── instance/          # Database & Local Storage
├── .env               # Environment configuration
├── config.py          # Static settings
├── login_credentials.txt # Institutional access registry
├── requirements.txt   # Dependencies
└── run.py             # Entry sequence
```
