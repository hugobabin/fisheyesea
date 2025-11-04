![fisheyeseabanner](https://repository-images.githubusercontent.com/1076189935/6fb63ac3-2b4d-463b-ae0d-96168ec9195e)  
[![GitHub](https://img.shields.io/badge/Hugo%20Babin-%23121011.svg?logo=github&logoColor=white)](https://github.com/hugobabin) [![fisheyesea](https://img.shields.io/badge/fisheyesea_0.1-59A8C9)](https://github.com/hugobabin/fisheyesea) **|** [![Python](https://img.shields.io/badge/Python_3.12-3776AB?logo=python&logoColor=fff)](#) [![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](#) [![MariaDB](https://img.shields.io/badge/MariaDB-003545?logo=mariadb&logoColor=white)](#) [![DuckDB](https://img.shields.io/badge/DuckDB-000?logo=duckdb&logoColor=yellow)](#) **|** [![UV](https://img.shields.io/badge/UV-30173d?logo=uv)](#)
##### fisheyesea version 0.1 - no UI yet, only accessible through fastapi docs
##### This software is accessible via your navigator and allows you to get access to centralized informations from different sources about the overuse of sea-based resource.
##### This project was made possible thanks to the following data providers : ***data.worldbank.org*** - ***globalfishingwatch.org*** - ***database.earth*** - ***ourworldindata.org*** - ***fao.org***
## Compatibility
fisheyesea is only available for LINUX distributions, not available for Windows !
## How to install
**➪** make sure you have python 3.12 installed (https://www.python.org/downloads/)  
**➪** command: *git clone* https://github.com/hugobabin/fisheyesea **specify_folder_if_needed**  
**➪** command: *cd* **your_folder**  
**➪** command: *make setup*  
**➪** here you go !

(if you're using the ETL, don't forget to get your globalfishingwatch API key here https://globalfishingwatch.org/our-apis/documentation#quick-start, and paste it in your config/.env file at API_TOKEN=yourapitoken)

## My recommendations
WIP

## How to use (different commands)
**➪** first, **docker compose up** (important in order to start mariadb) at the project's root  
**➪** **make run** - launches the app  
**➪** **make run_etl** - launches both the app and the etl process  
**➪** **make etl** - only launches the etl process  
*other commands are listed in the project's Makefile*

