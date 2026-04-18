#!/usr/bin/env python
# 测试Python环境和依赖项

import sys
import os

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# 测试导入必要的模块
try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except Exception as e:
    print(f"Error importing fastapi: {str(e)}")

try:
    import uvicorn
    print(f"Uvicorn version: {uvicorn.__version__}")
except Exception as e:
    print(f"Error importing uvicorn: {str(e)}")

try:
    import sqlalchemy
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
except Exception as e:
    print(f"Error importing sqlalchemy: {str(e)}")

try:
    import pymysql
    print(f"PyMySQL version: {pymysql.__version__}")
except Exception as e:
    print(f"Error importing pymysql: {str(e)}")

try:
    import langgraph
    print(f"LangGraph version: {langgraph.__version__}")
except Exception as e:
    print(f"Error importing langgraph: {str(e)}")

try:
    import dotenv
    print(f"Dotenv version: {dotenv.__version__}")
except Exception as e:
    print(f"Error importing dotenv: {str(e)}")

# 测试导入本地模块
try:
    from ai.state import UserState
    print("Successfully imported UserState")
except Exception as e:
    print(f"Error importing UserState: {str(e)}")

try:
    from ai.workflow import create_workflow
    print("Successfully imported create_workflow")
except Exception as e:
    print(f"Error importing create_workflow: {str(e)}")

try:
    from backend.database import get_db, engine, Base
    print("Successfully imported database modules")
except Exception as e:
    print(f"Error importing database modules: {str(e)}")

print("Environment test completed.")
