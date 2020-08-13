from app.entities.DB2QueryEntity import DB2QueryEntity
import ibm_db_dbi as db
import time
import os
import pandas as pd
from datetime import datetime
from threading import Thread


class ConnectionsComponent:
    def __init__(self, log_dir):
        self.enable_connection_summary = False
        self.connection_summary_entity = None
        self.log_dir = log_dir

    def enable_connection_summary_task(self, entity: DB2QueryEntity):
        if not self.enable_connection_summary:
            self.connection_summary_entity = entity
            self.enable_connection_summary = True
            thread = Thread(target=self.__connection_summary, args=(entity,))
            thread.daemon = True
            thread.start()

    def disable_connection_summary_task(self):
        self.enable_connection_summary = False

    def __connection_summary(self, entity: DB2QueryEntity):
        conn = None
        columns = ["APPLICATION_HANDLE", "APPLICATION_NAME", "TOTAL_APP_COMMITS", "TOTAL_APP_ROLLBACKS",
                   "ACT_COMPLETED_TOTAL", "APP_RQSTS_COMPLETED_TOTAL", "AVG_RQST_CPU_TIME", "ROUTINE_TIME_RQST_PERCENT",
                   "RQST_WAIT_TIME_PERCENT", "ACT_WAIT_TIME_PERCENT", "IO_WAIT_TIME_PERCENT",
                   "LOCK_WAIT_TIME_PERCENT", "AGENT_WAIT_TIME_PERCENT", "NETWORK_WAIT_TIME_PERCENT",
                   "SECTION_PROC_TIME_PERCENT", "SECTION_SORT_PROC_TIME_PERCENT",
                   "COMPILE_PROC_TIME_PERCENT", "TRANSACT_END_PROC_TIME_PERCENT",
                   "UTILS_PROC_TIME_PERCENT", "AVG_LOCK_WAITS_PER_ACT",
                   "AVG_LOCK_TIMEOUTS_PER_ACT", "AVG_DEADLOCKS_PER_ACT",
                   "AVG_LOCK_ESCALS_PER_ACT", "ROWS_READ_PER_ROWS_RETURNED"]
        select = "SELECT {} FROM SYSIBMADM.MON_CONNECTION_SUMMARY".format(",".join(columns).rstrip(','))
        try:
            conn = db.connect(entity.get_connection(), "", "")
            while self.enable_connection_summary:
                date = datetime.now()
                print("read {} at {}".format(entity.database, date))
                cursor = conn.cursor()
                cursor.execute(select)
                data = list()
                for r in cursor.fetchall():
                    data.append(r)
                df = pd.DataFrame(data, columns=columns )
                df.to_csv(os.path.join(self.log_dir,
                                       'sen_db2_con_summa_{}_{}_{}_{}.csv'.format(date.day, date.hour, date.minute,
                                                                                   date.second)),
                          index=False)
                time.sleep(entity.interval)
                cursor.close()
        except Exception as e:
            print(e)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as e:
                    print(e)

