# Bank-app
Projekt - Testowanie Automatyczne


**Author:**
- **Name:** Rafał Mazurek
- **Group:** 4

---

## How to start the app

### 1. Prerequisites
Ensure you have the following installed:
- **Python 3.x**
- **Docker**

### 2. Environment Setup
Navigate to the application directory and install the required dependencies:

```bash
cd BankApp/app
pip install -r requirements.txt
```

### 3. Start Database (MongoDB)
The application requires a running MongoDB. Start it using Docker from the project root directory:

```bash
docker compose -f mongo.yml up -d
```

### 4. Run the Flask Server
To start the application server, run the following commands from the `BankApp/app` directory:

```bash
export FLASK_APP=api.py
flask run
```

The application will be available at:
http://127.0.0.1:5000

---

## How to execute tests

### 1. Unit & Integration Tests

```bash
python3 -m pytest tests
```

### 2. BDD Tests (Gherkin)

```bash
behave
```

### 3. Performance Tests

```bash
python3 -m pytest tests/perf
```