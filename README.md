# evs_blockchain_min  

A minimal **Election Voting System** built on top of a simple blockchain.  
The project demonstrates how blockchain concepts can be integrated into a Django application to provide tamper‑evident vote storage.

---

## Overview  

`evs_blockchain_min` is a lightweight Django app that models an election where each vote is recorded as a block in a private blockchain. The blockchain ensures:

* **Immutability** – once a vote is added, its hash cannot be altered without breaking the chain.  
* **Transparency** – the full chain can be inspected via the admin interface or API.  
* **Simplicity** – the implementation focuses on core blockchain mechanics (hashing, nonce, proof‑of‑work) without the overhead of a full‑node network.

The repository contains the core Django components (`models`, `views`, `urls`) and a self‑contained blockchain implementation (`blockchain.py`).

---

## Features  

| ✅ | Feature |
|---|---------|
| ✅ | **Block creation** with proof‑of‑work (nonce) and SHA‑256 hashing |
| ✅ | **Vote model** linked to a `Block` (candidate, election, timestamp) |
| ✅ | **Admin UI** for inspecting blocks, votes, and blockchain status |
| ✅ | **REST‑style endpoints** (`/api/blocks/`, `/api/votes/`) for programmatic interaction |
| ✅ | **Database migrations** covering schema evolution from the initial model to the final block structure |
| ✅ | **Modular design** – blockchain logic isolated in `evs/blockchain.py` for easy reuse |

---

## Tech Stack  

| Component | Version / Tool |
|-----------|----------------|
| Python | 3.9+ |
| Django | 4.x (as defined in `requirements.txt`) |
| SQLite (default) | – |
| Git | – |
| SHA‑256 (hashlib) | – |

*All blockchain operations are performed with Python’s standard library (`hashlib`, `datetime`). No external blockchain libraries are required.*

---

## Installation  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/evs_blockchain_min.git
cd evs_blockchain_min

# 2️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt   # (Django and any additional packages)

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create a superuser for the admin interface
python manage.py createsuperuser
```

> **Note:** If a `requirements.txt` file is missing, you can start with `pip install Django==4.*`.

---

## Usage  

### Run the development server  

```bash
python manage.py runserver
```

* The admin panel is available at `http://127.0.0.1:8000/admin/`.  
* API endpoints (example)  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/blocks/` | List all blocks in the chain |
| `POST` | `/api/votes/` | Submit a new vote (creates a new block) |
| `GET` | `/api/votes/<id>/` | Retrieve a specific vote |

### Example: Adding a vote via the API  

```bash