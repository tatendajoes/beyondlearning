from sqlalchemy import (
    create_engine, Column, String, Integer, Time, Boolean, MetaData, Table, ForeignKey, Date
)
from datetime import datetime
import pandas as pd
import uuid, json

# ---- DB class-------------------------------------------------------------------------

class ClassRecord:
    def __init__(self,db_url="sqlite:///records.db"):
        self.engine  = create_engine(db_url, echo=False)
        self.metadata = MetaData()
        self.tables   = {}

    def initialize_db(self):
        # Create the classes table
        self.tables['classes'] = Table(
            "classes",
            self.metadata,
            Column("class_id",    String(32), primary_key=True),
            Column("class_name",  String(64), nullable=False),
            Column("class_level", Integer,    nullable=False),
            Column("instructor_name",  String(64), nullable=False),
            Column("has_session", Boolean,    nullable=False, default=False),)
        
    
    # Create the sessions tables
        self.tables['sessions'] = Table(
                "sessions", self.metadata,
                Column("session_id",   String(36), primary_key=True),
                Column("class_id",     String(32), ForeignKey("classes.class_id")),
                Column("description",  String(128)),
                Column("date",         Date),
                Column("start_time",   Time),
                Column("end_time",     Time),
                Column("attendance",   Integer),
            )

        # ── NEW: concentration logs (1-to-many to sessions) ────────────
        self.tables['concentration_logs'] = Table(
            "concentration_logs", self.metadata,
            Column("log_id",      String(36), primary_key=True),
            Column("session_id",  String(36), ForeignKey("sessions.session_id")),
            Column("timestamp_ms", Integer),
            Column("score",        Integer),
        )
        self.metadata.create_all(self.engine)

    

    def insert_row(self, cid, name, level, name2, has_session=False):
        with self.engine.begin() as c:
            c.execute(
                self.tables['classes'].insert().prefix_with("OR IGNORE"),
                {
                    "class_id": cid,
                    "class_name": name,
                    "class_level": int(level),
                    "instructor_name": name2,
                    "has_session": bool(has_session),
                },
            )
    def insert_session(self, **kw):
        kw["session_id"] = kw.get("session_id") or str(uuid.uuid4())
        with self.engine.begin() as c:
            c.execute(self.tables['sessions'].insert(), kw)
        # create an empty concentration log placeholder
        self.insert_concentration(kw["session_id"], 0, 0)
        return kw["session_id"]

    def insert_concentration(self, session_id, timestamp_ms, score):
        with self.engine.begin() as c:
            c.execute(self.tables['concentration_logs'].insert(), {
                "log_id": str(uuid.uuid4()),
                "session_id": session_id,
                "timestamp_ms": int(timestamp_ms),
                "score": int(score),
            })

    def fetch_all(self, table_id):
        if table_id == 1:
            return pd.read_sql(self.tables['classes'].select(), self.engine)
        elif table_id == 2:
            return pd.read_sql(self.tables['sessions'].select(), self.engine)
        elif table_id == 3: 
            return pd.read_sql(self.tables['concentration_logs'].select(), self.engine)
        else:
            return pd.DataFrame()
    def delete_row(self, cid):
        with self.engine.begin() as c:
            c.execute(self.tables['classes'].delete().where(
                self.tables['classes'].c.class_id == cid
            ))