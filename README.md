# Tử Vi Web App

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.7-green.svg)

**Vietnamese Astrology Web Application - Create and manage Tử Vi natal charts**

[Features](#features) • [Quick Start](#quick-start) • [API](#api-reference) 

</div>

---

## About

Tử Vi Web App is a web application for creating and managing Vietnamese astrology natal charts (Tử Vi/紫微斗數). The application performs accurate astrological calculations based on birth information (date, time, and gender), supports both Lunar and Solar calendars, and provides comprehensive chart management features including folder organization and favorites.

## Features

- 🎯 Accurate natal chart calculation (Lunar & Solar calendars)
- 💾 Save and manage multiple charts
- 📁 Organize charts by folders
- ⭐ Favorite marking system
- 🎨 Modern, responsive UI
- 👁️ List view for chart management
- ✏️ Edit chart information directly
- 🌐 RESTful API

## Quick Start

```bash
# 1. Clone and navigate
git clone <repository-url>
cd tuvi_web_app

# 2. Setup environment (requires uv)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 3. Initialize and run
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000 in your browser.

> **Note**: Install [uv](https://github.com/astral-sh/uv) first: `pip install uv`

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Tech Stack](#tech-stack)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package installer

### Detailed Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tuvi_web_app
   ```

2. **Install uv** (if not already installed)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or via pip
   pip install uv
   ```

3. **Create virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

4. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create admin user** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Main Pages

- **Home** (`/`) - Manage all saved charts
- **New Chart** (`/new/`) - Create a new natal chart
- **Admin Panel** (`/admin/`) - Django admin interface

### Creating a Chart

1. Navigate to `/new/`
2. Enter birth information:
   - Name (optional)
   - Gender
   - Date of birth (day, month, year)
   - Time of birth (hour)
   - Timezone (default: GMT+7)
   - Calendar type (Lunar/Solar)
3. Click "Lập lá số" (Create Chart)

### Managing Charts

- **Save**: Click 💾 button after creating a chart
- **Favorite**: Click ❤️ to mark as favorite (border turns yellow)
- **Move**: Click 📁 to move to a different folder
- **Delete**: Click delete button to remove

## Project Structure

```
tuvi_web_app/
├── backend/              # Django configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── tuvi/            # Main application
│       ├── models.py    # Data models
│       ├── views.py     # Views & API
│       ├── templates/   # HTML templates
│       └── static/      # CSS & JavaScript
├── core/
│   └── calculations/    # Astrology calculation engine
├── manage.py
├── db.sqlite3
└── requirements.txt
```

## API Reference

### Chart Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api` | Calculate natal chart |

**Parameters**: `hoten`, `gioitinh`, `ngaysinh`, `thangsinh`, `namsinh`, `giosinh`, `muigio`, `amlich`

### Chart Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/save-laso/` | Save or update chart |
| GET | `/api/lasos/?filter={filter}` | List charts (`all`, `favorites`, `folder_{id}`) |
| GET | `/api/laso/<id>/` | Get chart details |
| POST | `/api/laso/<id>/toggle-favorite/` | Toggle favorite status |
| POST | `/api/laso/<id>/move/` | Move to folder |
| DELETE | `/api/laso/<id>/delete/` | Delete chart |

### Folder Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/folders/` | List all folders |
| DELETE | `/api/folder/<id>/delete/` | Delete folder |

## Tech Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite3
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Calculations**: PyEphem (astronomical calculations)
- **Architecture**: Django Monolith

## License

This project is licensed under the MIT License.

## Acknowledgments

- [PyEphem](https://rhodesmill.org/pyephem/) - Astronomical calculations
- [Django](https://www.djangoproject.com/) - Web framework
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

---

<div align="center">

Made with ❤️ by [Thanh Tung Vu](mailto:tungvu.telecom@gmail.com)

</div>
