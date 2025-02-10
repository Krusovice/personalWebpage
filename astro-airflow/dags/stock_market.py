from airflow.decorators import dag, task
from datetime import datetime
from airflow.sensors.base import PokeReturnValue
from airflow.hooks.base import BaseHook
#from airflow.operators import PythonOperator


@dag(
	start_date=datetime(2025,2,10),
	schedule='@daily',
	catchup=False,
	tags=['stock_market'],

)

def stock_market():
	
	@task.sensor(poke_interval=30, timeout=300, mode='poke')
	def is_api_available() -> PokeReturnValue:
		import requests

		api = BaseHook.get_connection('stock_api')
		url = f"{api.host}{api.extra_dejson['endpoint']}"
		print(url)
		response = requests.get(url, headers=api.extra_dejson['headers'])

		condition = response.json()['finance']['result'] is None
		return PokeReturnValue(is_done=condition, xcom_value=url)

	is_api_available()

stock_market()