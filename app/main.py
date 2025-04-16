from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import os

app = FastAPI()


class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str

TUSHARE_TOKEN = "58dbbc660d3951a4e272b87014204c98e903c50b65183e30c4c8c2e2"

@app.post("/backtest")
def run_backtest(request: BacktestRequest):
    try:
        result = subprocess.run([
            "python", "backtest/runner.py",
            request.symbol, request.start_date, request.end_date, TUSHARE_TOKEN
        ], check=True, capture_output=True, text=True)
        # print("stdout:", result.stdout)
        # print("stderr:", result.stderr)
        return {"message": "Backtest completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/result")
def get_result():
    try:
        with open("backtest/result.json", "r") as f:
            result = json.load(f)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No result available")