# app/api/v1/routes/reports.py

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.session_dep import require_session
from app.db.connection import fetch_all

router = APIRouter(prefix="/reports", tags=["Reports"])

