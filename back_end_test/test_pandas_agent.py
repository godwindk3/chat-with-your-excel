import os
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                google_api_key=google_api_key)

df = pd.read_excel("./data/data.xlsx", sheet_name="Đơn hàng vận chuyển")

colulm_description = pd.read_excel("./data/data.xlsx", sheet_name="Mô tả trường thông tin")

colulm_description_str = colulm_description.to_string(index=False)

df["Thời gian thực tế rời điểm lấy"] = pd.to_datetime(df["Thời gian thực tế rời điểm lấy"], errors="coerce")


prefix_text = (
    "You are a data analyst. Analyze the dataframe named df and provide concise answers. \n"
    "Here is the column description:\n"
    f"{colulm_description_str}"
)

agent = create_pandas_dataframe_agent(
    model,
    df,
    agent_type="tool-calling",
    allow_dangerous_code=True,
    verbose=True,
    prefix=prefix_text,
    suffix="Provide the final answer in a clear and structured format.",
)
response = agent.invoke("Số lượng hàng vận chuyển xuất bán trong tháng 6 là bao nhiêu?")
print(response["output"])