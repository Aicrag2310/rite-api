from setuptools import find_packages, setup

setup(
    name='rite-api',
    version='1.0.0',
    packages=find_packages(exclude=('test', 'test.*', 'tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "python-dotenv",
        "fastapi==0.99.*",
        "ujson==5.7.0",
        "email-validator==1.3.1",
        "uvicorn==0.20.0",
        "python-jose[cryptography]==3.3.*",
        "passlib[bcrypt]==1.7.*",
        "python-multipart==0.0.6",
        "mysqlclient==2.1.1",
        "SQLAlchemy==1.4.40",
        "SQLAlchemy-Utils==0.38.2",
        "python-i18n[YAML]",
        "openpyxl==3.1.2",
        "pyodbc==5.1.0",
        "alembic==1.9.*",
        "pytz==2024.1",
        "python-dateutil==2.9.0.post0",
    ],
)
