
### Scripts Directory

#### `/scripts/init_db.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.stock_data import Base

engine = create_engine('sqlite:///stocks.db')
Base.metadata.create_all(engine)
print("Database initialized.")
