import papermill as pm
from datetime import datetime

curr_date = datetime.now().strftime("%Y-%m-%d")

pm.execute_notebook(
   'docs/stock_analysis_template.ipynb',
   'docs/brag_02_20_2023.ipynb',
   parameters=dict(ticker="BRAG.TO", start_date="2019-04-01", end_date=curr_date)
)