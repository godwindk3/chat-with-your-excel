import os
from typing import Optional

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

from app.core.config import settings
from app.services.storage import find_file_by_id
from app.services.preprocess import read_and_preprocess_sheet


router = APIRouter(tags=["analyze"])


class AnalyzeRequest(BaseModel):
    fileId: str
    sheetName: str
    question: str


class AnalyzeResponse(BaseModel):
    output: str


def build_agent_for_file(file_path: str, sheet_name: str):
    load_dotenv()  # load GOOGLE_API_KEY if present
    google_api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured")

    # Read target sheet
    try:
        df = read_and_preprocess_sheet(file_path, sheet_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read sheet '{sheet_name}': {e}")

    # Optional: read description sheet and inject into prefix
    try:
        if "Mô tả trường thông tin" in pd.ExcelFile(file_path).sheet_names:
            col_desc_df = pd.read_excel(file_path, sheet_name="Mô tả trường thông tin")
            col_desc_str = col_desc_df.to_string(index=False)
        else:
            col_desc_str = None
    except Exception:
        col_desc_str = None

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

    base_prefix = "You are a data analyst. Analyze the dataframe named df and provide concise answers. \n"
    if col_desc_str:
        prefix_text = base_prefix + "Here is the column description:\n" + col_desc_str
    else:
        prefix_text = base_prefix

    # Note: Column-specific handling is no longer hard-coded; preprocessing handles mixed types and dates.

    agent = create_pandas_dataframe_agent(
        model,
        df,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        verbose=False,
        prefix=prefix_text,
        suffix="Provide the final answer in a clear and structured format.",
    )

    return agent


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    file_path = find_file_by_id(req.fileId)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    agent = build_agent_for_file(file_path, req.sheetName)
    try:
        response = agent.invoke(req.question)
        output = response.get("output") if isinstance(response, dict) else str(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    return AnalyzeResponse(output=output)


