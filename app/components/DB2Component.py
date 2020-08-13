from app.entities.DB2ConnectionEntity import DB2ConnectionEntity
import ibm_db_dbi as db


class DB2Component:

    @staticmethod
    def validate_connection(entity: DB2ConnectionEntity):
        conn = None
        try:
            conn = db.connect(entity.get_connection(), "", "")
            cursor = conn.cursor()
            cursor.execute("SELECT service_level FROM  TABLE(sysproc.env_get_inst_info()) as INSTANCEINFO")
            cursor.fetchall()
            cursor.close()
            return True
        except Exception as e:
            raise ValueError(entity.get_connection()) from e
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    raise ValueError("Close Exception {}".format(entity.get_connection()))
