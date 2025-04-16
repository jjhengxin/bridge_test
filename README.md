### 文件结构：

strategy_backtest_fastapi/

├── app/

│   └── main.py             # FastAPI 后端接口（POST /backtest + GET /result）

├── backtest/

│   ├── strategy.py         # 均线交叉策略

│   ├── runner.py           # 回测执行器（调用 Tushare 获取数据 + 回测 + 保存结果）

│   └── result.json         # 回测结果输出文件

├── requirements.txt        # 所需依赖包

### 使用说明：
下载代码后，执行

` pip install -r requirements.txt `
 
` uvicorn app.main:app --reload `

然后，在一个新的shell中执行

` curl.exe -X POST "http://127.0.0.1:8000/backtest" -H "Content-Type: application/json" -d "{\"symbol\": \"000001.SZ\", \"start_date\": \"2023-01-01\", \"end_date\": \"2023-12-31\"}" `

确认返回信息为“Backtest completed”后继续执行

`curl http://127.0.0.1:8000/result`

### 预期结果：
![image](https://github.com/user-attachments/assets/aa29247b-dcb3-49df-8291-2c467221e8f9)

![image](https://github.com/user-attachments/assets/39ccb177-beab-4e2e-83f3-d140d79d64e3)
