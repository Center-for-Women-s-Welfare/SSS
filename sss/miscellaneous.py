# import packages
import pandas as pd
import preprocess

# read file with miscellaneous
# note: 6 tables have broadband, here is one example
AR2022 = pd.read_excel("data/CA2022_SSS_Partial.xlsx",sheet_name = "By Family")
AR2022_clean_col = perprocess.std_col_names(AR2022)

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
class Miscellaneous(Base):
    __tablename__ = "miscellaneous"
    family_type = Column("family_type", String, primary_key = True)
    place = Column("place", String, primary_key = True)
    state = Column("state", String, primary_key = True)
    year = Column("year", String, primary_key = True)
    analysis =  Column("analysis", String, primary_key = True)
    broadband_and_cell_phone = Column("broadband_and_cell_phone", Float)
    other_necessities = Column("other_necessities", Float)

# create a table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# create a session
session = Session()

# map the excel file to the database
session.bulk_insert_mappings(Miscellaneous,AR2022_clean_col.to_dict(orient="records"))

session.commit()

