# Hospital Management System (HMS) - MAD II Project


---

### Backend
*   **Framework:** Flask (Python)
*   **Database:** SQLite via Flask-SQLAlchemy
*   **Authentication:** JWT (JSON Web Tokens) via Flask-JWT-Extended
*   **Background Jobs:** Celery & Redis
*   **Email Server Tooling:** MailHog (for local testing/demonstration)
*   **Caching:** Flask-Caching with Redis

### Frontend
*   **Framework:** Vue.js 3 (Composition API)
*   **Routing:** Vue Router
*   **Styling:** Bootstrap 5

---

##  Advanced Features (Viva Talking Points)

1.  **Role-Based Access Control (RBAC):** Backend API is heavily protected using `@jwt_required()` decorators and custom guard functions (`is_admin()`, `is_doctor()`, `is_patient()`). The frontend Vue Router mirrors this by utilizing navigation guards (`beforeEach()`).
2.  **Redis Separation:** The application uses two separate Redis databases to prevent concurrency issues:
    *   `DB 0` is used by Celery as the Message Broker and Result Backend.
    *   `DB 2` is used by Flask-Caching for the API endpoints.
3.  **Cache Invalidation Validation:** When an Admin creates/deletes a department, doctor, or patient, the system explicitly calls `cache.delete()` against the cached Redis keys (`admin_dashboard`, `department_list`) to heavily prevent stale UI data.
4.  **Scheduled Background Tasks (Celery Beat):**
    *   **Daily Reminder:** Triggers daily at `16:53` (or customizable time). Queries the database for all appointments scheduled for *today*, and automatically emails a beautifully formatted HTML reminder to the patient.
    *   **Monthly Report:** Triggers on the 2nd of every month. Queries the entire last month's data, compiles an overarching activity report for *each doctor* (Total, Completed, Cancelled, Diagnoses list), and emails an HTML summary.

---

## How to Run the Project (Local Installation)

You will need **Python 3.10+**, **Node.js 18+**, **Redis**, and **MailHog** installed. 
A convenient script (`start.sh`) is provided to launch everything simultaneously on WSL/Linux environments. If starting manually, follow the 5 discrete components below:

### 1. Start Redis
```bash
redis-server
```

### 2. Start MailHog 
*It is recommended to run MailHog on port `8025` for the UI, and port `1025` for the SMTP server.*
```bash
# Example if using Go binary
~/go/bin/MailHog
```

### 3. Start the Flask Backend
```bash
cd backend
# Create environment, activate, install requirements if first time
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

# Run app
python app.py
```
*Note: The database (`instance/hms.db`) automatically populates Admin credentials (`admin@admin.com` / `admin@admin.com`) on first initialization.*

### 4. Start Celery (Worker & Beat)
Open two separate terminals in the `backend/` directory with the `.env` activated:

**Terminal A (Worker):**
```bash
celery -A celery_app worker --loglevel=info
```
**Terminal B (Beat Scheduler):**
```bash
celery -A celery_app beat --loglevel=info
```

### 5. Start the Vue Frontend
```bash
cd frontend
npm install # if first time
npm run dev
```

The frontend will be accessible at [http://localhost:5173](http://localhost:5173) and the API will serve from [http://127.0.0.1:5000](http://127.0.0.1:5000). You can monitor outgoing background emails by navigating to the MailHog UI at [http://localhost:8025](http://localhost:8025).
