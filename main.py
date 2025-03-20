import json
import requests
import time
from requests.auth import HTTPBasicAuth

endpoint=""

url = "%s/api/prom/api/v1/label/__name__/values"%endpoint
username=""
api_key=""

response = requests.get(
      url,
      auth=HTTPBasicAuth(username, api_key)
  )

data = response.json()

query_url = "%s/api/prom/api/v1/query"%endpoint
filtered_metrics = [
    metric for metric in data['data'] 
    if not any(metric.endswith(suffix) for suffix in ['_count', '_bucket', '_sum'])
]
with open("metric_rates.txt", "w") as f:
  for metric in filtered_metrics:
    metric_name = metric
    query = f"count_over_time({metric_name}[5m])/5"
    query_response = requests.get(
        query_url,
        auth=HTTPBasicAuth(username, api_key),
        params={"query": query}
    )
    query_data = query_response.json().get( "data", {}).get("result", [])
    if query_data and len(query_data) > 0 and len(query_data[0].get('value', [])) > 1:
      dpm=(query_data[0]['value'][1])
      if float(dpm) > 1:
        print(metric_name, dpm)
        f.write(f"{metric_name} {dpm}\n")
    else:
      continue

