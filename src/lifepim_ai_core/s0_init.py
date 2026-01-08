from db import create_schema, create_schema_memory
import os
from core.llm_runtime import config as cfg



if __name__ == "__main__":
    try:
        os.remove(cfg.DB_FILE_METADATA)
    except:
        print('Cant delete database file!')
        pass
    create_schema(cfg.DB_FILE_METADATA)

    # create a blank memory database if it doesnt exist
    create_schema_memory(cfg.DB_FILE)
