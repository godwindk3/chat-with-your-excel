import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                google_api_key="YOUR_GOOGLE_API_KEY")

df = pd.read_excel("./data/data_wms_ttc.xlsx", sheet_name="Data tồn kho")

agent = create_pandas_dataframe_agent(
    model,
    df,
    agent_type="tool-calling",
    allow_dangerous_code=True,
    verbose=True,
    prefix="You are a data analyst. Analyze the dataframe name df and provide concise answers.",
    suffix="Provide the final answer in a clear and structured format.",
)
response = agent.invoke("Khu vực nào có lượng hàng tồn kho cao nhất hiện tại")
print(response["output"])