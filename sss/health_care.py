# import packages
import pandas as pd
import preprocess


# read file with health costs 
health_cost = pd.read_excel("data/OR2021_SSS_ARPA_Partial.xlsx",sheet_name = "By Family")

# standardize the column names 
health_cost_clean_col = preprocess.std_col_names(health_cost)

from sqlalchemy import (create_engine, MetaData, 
                        Table, Column, 
                        Integer, String, 
                        Float, ForeignKey)
from sqlalchemy.orm import declarative_base

# create engine 
engine = create_engine("sqlite:///sss.sqlite", echo = False)
m = MetaData(bind=engine)
Base = declarative_base(metadata=m)

# declare table columns and data type
class HealthCare(Base):
    __tablename__ = "health_care"
    family_type = Column("family_type", String, primary_key = True)
    state = Column("state", String, primary_key = True)
    place = Column("place", String, primary_key = True)
    year = Column("year", Integer, primary_key = True)
    analysis =  Column("analysis", String, primary_key = True)
    premium = Column("premium", Float)
    out_of_pocket = Column("out_of_pocket", Float)

# create a table
Base.metadata.create_all(engine)

from sqlalchemy.orm.session import sessionmaker

# create a session
session = Session()

# map the excel file to the database
session.bulk_insert_mappings(HealthCare,health_cost_clean_col.to_dict(orient="records"))

session.commit()
