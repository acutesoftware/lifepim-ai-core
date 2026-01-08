import os
import time
from datetime import datetime
from lifepim_ai_core.db import insert_many_files
from lifepim_ai_core.core.llm_runtime import config as cfg

def get_file_owner(file_path):
    """
            # Owner lookup
        sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
        file_owner = f"{domain}\\{name}"
    """
    return r"domain\\user_TODO"


def collect_files(folder_path: str, db_path: str):
    """
    Scan the folder recursively and insert/update file metadata into the database.
    """
    print(f"📂 Scanning folder: {folder_path}")
    file_count = 0
    lst_metadata = []
    for root, _, files in os.walk(folder_path):
        print('scanning ' + root)
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                stat = os.stat(fpath)
                """
                file_metadata = {
                    "file_path": os.path.abspath(fpath),
                    "file_name": fname,
                    "file_type": os.path.splitext(fname)[1].lower(),
                    "file_size": stat.st_size,
                    "date_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "date_created": datetime.fromtimestamp(stat.st_ctime).isoformat() if os.name == "nt" else None,
                    "date_accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                    "file_owner": get_file_owner(fpath)               
                }
                """
                
                file_metadata = [
                    os.path.abspath(fpath),
                    fname,
                    os.path.splitext(fname)[1].lower(),
                    stat.st_size,
                    datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    datetime.fromtimestamp(stat.st_ctime).isoformat() if os.name == "nt" else None,
                    datetime.fromtimestamp(stat.st_atime).isoformat(),
                    get_file_owner(fpath)               
                ]
                lst_metadata.append(file_metadata)
                #print(f"Added/Updated: {fname} (id={file_id})")
                file_count += 1

            except Exception as e:
                print(f"Error processing {fpath}: {e}")
    insert_many_files(db_path, lst_metadata)

    print(f"Completed. {file_count} files indexed.")


if __name__ == "__main__":
    start = time.time()
    collect_files(cfg.DOCS_FOLDER, cfg.DB_FILE_METADATA)
    print(f"Done in {time.time()-start:.2f}s")
