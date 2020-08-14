from app.components.ConfigurationComponent import ConfigurationComponent
import ibm_db_dbi as db
import time
import os
import pandas as pd
import logging
from datetime import datetime
from threading import Thread


class ConnectionsAgent:

    @staticmethod
    def connection_summary():
        thread = Thread(target=ConnectionsAgent.__connection_summary, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    def __connection_summary():
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
            conn = db.connect(ConfigurationComponent.get_connection(), "", "")
            while True:
                date = datetime.now()
                logging.info("read {} at {}".format(ConfigurationComponent.get_connection(), date))
                cursor = None
                try:
                    cursor = conn.cursor()
                    cursor.execute(select)
                    data = list()
                    for r in cursor.fetchall():
                        data.append(r)
                    df = pd.DataFrame(data, columns=columns)
                    df.to_csv(os.path.join(ConfigurationComponent.get_log_dir(),
                                           '{}_sen_db2_con_summa_{}_{}_{}_{}.csv'.format(ConfigurationComponent.get_trace_name(),
                                                                                         date.day,
                                                                                         date.hour,
                                                                                         date.minute,
                                                                                         date.second)),
                              index=False)

                    time.sleep(ConfigurationComponent.get_interval())

                except Exception as e:
                    logging.info(e)
                finally:
                    cursor.close()

        except Exception as e:
            logging.info(e)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception as ee:
                    logging.info(ee)
