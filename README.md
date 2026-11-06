\# AI Business Studio



\*\*AI-Powered Business Automation Platform\*\*



AI Business Studio is a web-based business automation platform built with Python and FastAPI. It combines invoice analysis and automated website generation in one application.



\## Features



\### 1. Invoice Analyzer

\- Upload invoice documents.

\- Extract invoice information.

\- Process invoice data.

\- Store invoice records in MySQL.



\### 2. Website Generator

\- Generate website HTML.

\- Generate CSS styling.

\- Generate JavaScript functionality.

\- Preview generated websites.

\- Download generated websites as ZIP files.



\### 3. Dashboard

\- Manage invoice records.

\- View generated websites.

\- Access application features through a web interface.



\## Technology Stack



| Component | Technology |

|---|---|

| Backend | Python, FastAPI |

| Database | MySQL |

| ORM | SQLAlchemy |

| Frontend | HTML, CSS, JavaScript |

| API Documentation | Swagger UI |

| Version Control | Git, GitHub |



\## Project Structure



```text

AI-Invoice-Analyzer/

│

├── app/

│   ├── database/

│   ├── models/

│   ├── routers/

│   ├── services/

│   └── static/

│

├── requirements.txt

├── test\_extract.py

├── .gitignore

└── README.md

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/Indira177/ai-business-studio.git

cd ai-business-studio

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the environment



Windows:



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Configure environment variables



Create a `.env` file in the project root:



```env

DATABASE\_URL=mysql+pymysql://YOUR\_USERNAME:YOUR\_PASSWORD@localhost:3306/invoice\_analyzer\_db

```



Replace the placeholders with your own MySQL credentials.



Make sure the MySQL database exists before starting the application.



\### 6. Run the application



```bash

python -m uvicorn app.main:app --reload

```



\### 7. Open the application



Application:



http://127.0.0.1:8000



API documentation:



http://127.0.0.1:8000/docs



\## Security



\- Database credentials are stored in environment variables.

\- `.env` files are excluded through `.gitignore`.

\- Virtual environments are excluded from version control.

\- Uploaded documents are excluded from the public repository.



\## Future Enhancements



\- AI-powered invoice data extraction improvements.

\- Automated email notifications.

\- Website hosting and publishing.

\- Advanced business analytics.

\- User authentication and role management.



\## Developer



\*\*NextGen Project Lab\*\*



GitHub: https://github.com/Indira177



\---



\*AI Business Studio – Simplifying Business Automation.\*



