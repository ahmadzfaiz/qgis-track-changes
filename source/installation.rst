Installation Guide
==================

Follow these steps to install QGIS Track Changes.

Prerequisites
-------------
Ensure you have the following installed:
- Python 3.7+
- QGIS
- GDAL
- Virtual environment (recommended)

Installation Steps
------------------
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/qgis-track-changes.git
   cd qgis-track-changes
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```