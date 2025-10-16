run:
	@bash launch.bash

run_etl:
	@bash launch-with-etl.bash

run_etl_skip_api:
	@ETL_API_DISABLED=true bash launch-with-etl.bash

run_etl_skip_csv:
	@ETL_CSV_DISABLED=true bash launch-with-etl.bash

run_etl_skip_webscrap:
	@ETL_WEBSCRAP_DISABLED=true bash launch-with-etl.bash

run_etl_skip_mongo:
	@ETL_MONGO_DISABLED=true bash launch-with-etl.bash

# skip both mongo/api etl
run_etl_skip_bigdata:
	@ETL_MONGO_DISABLED=true ETL_API_DISABLED=true launch-with-etl.bash

# skip both csv/webscrap/sqlite etl
run_etl_skip_others:
	@ETL_CSV_DISABLED=true ETL_WEBSCRAP_DISABLED=true ETL_SQLITE_DISABLED=true launch-with-etl.bash
