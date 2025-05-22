# endgame

## 🧰 Requirements

- Docker & Docker Compose
- Python 3.11+
- pip or pipenv

## 🛠️ Local Setup

### 1. Clone the repository

### 2. Create a `.env` file

Create a `.env` file in the project root with the following variables:

```env
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=postgres
DB_PORT=5432

SECRET_KEY=your_secret_key
DEBUG=True
```

### 3. Start the PostgreSQL database using Docker

```bash
docker-compose up -d
```

This will:

- Start a PostgreSQL 15 container
- Expose it on `localhost:5432`

### 4. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 5. Apply migrations & create superuser

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to see your app running.

---

## ✅ Running Tests (TDD)

Tests are run using `pytest`.

```bash
pytest
```

---

## 📦 Deployment (AWS Elastic Beanstalk)

### 1. Environment Setup (One-time)

- Create an Elastic Beanstalk environment for your Django app.
- Attach an **RDS PostgreSQL instance**, or ensure your environment's **security group allows inbound access** to the RDS instance from the EB instance group.


### 2. Set Environment Variables in EB

You **must configure environment variables** in the Elastic Beanstalk environment (via the AWS Console or `eb setenv`) so that Django can connect to the RDS instance and run securely.

Example:

```bash
eb setenv DB_NAME=yourdbname DB_USER=youruser DB_PASSWORD=yourpassword DB_HOST=yourdbhost SECRET_KEY=your_secret DEBUG=False
```

These variables must match what your `settings.py` is expecting.

Alternatively, go to the **AWS EB Console > Configuration > Software > Environment properties** and set them manually.

### 3. GitHub Actions Deployment

Deployment is automated via GitHub Actions. The workflow:

- Runs tests on push to `main` or manually
- Deploys to Elastic Beanstalk if tests pass

### 4. AWS Authentication (OIDC)

Authentication into AWS is handled securely using **OpenID Connect (OIDC)** — no access keys or secrets needed.

**Steps to enable OIDC:**

1. In AWS IAM, create an IAM Role with:
   - A trust relationship for GitHub’s OIDC provider (`token.actions.githubusercontent.com`)
   - Conditions restricting it to your GitHub repository
   - The necessary policies (e.g., `ElasticBeanstalkFullAccess`, `AmazonRDSFullAccess`, etc.)

