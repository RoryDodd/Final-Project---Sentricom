# app/api/v1/routes/reports.py

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException