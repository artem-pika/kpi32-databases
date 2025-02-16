import psycopg2
import multiprocessing
import time

def exec_parallel(funcs, args_for_funcs):
    """Execute in parallel the given functions applied to corresponding arguments."""
    processes = []
    for func, args in zip(funcs, args_for_funcs):
        process = multiprocessing.Process(target=func, args=args)
        processes.append(process)
        process.start()
    
    # Wait until each process finishes its execution
    for process in processes:
        process.join()


def new_connection():
    conn = psycopg2.connect("dbname=lab1 user=postgres")
    cur = conn.cursor()
    return conn, cur

def init_table_values():
    conn, cur = new_connection()
    
    cur.execute("""DROP TABLE IF EXISTS user_counter;
    CREATE TABLE user_counter (
        user_id SERIAL PRIMARY KEY,
        counter INT,
        version INT
    );""")
    cur.execute("""INSERT INTO user_counter (user_id, counter, version)
    VALUES (1, 0, 0);""")
    conn.commit()
    
    cur.close()
    conn.close()

def check_table_values():
    conn, cur = new_connection()
    cur.execute("SELECT * FROM user_counter;")
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res

def exec_script_on_multiple_threads(script, n_threads=10):
    # Create different connections, each with corresponding script
    conns_and_curs = [new_connection() for _ in range(n_threads)]
    scripts = [script for _ in range(n_threads)]

    time_start = time.perf_counter()
    exec_parallel(scripts, conns_and_curs)
    time_end = time.perf_counter()
    time_spent = time_end - time_start

    for conn, cur in conns_and_curs:
        cur.close()
        conn.close()
    
    return time_spent


def exec_method(method_name, method_script):
    init_table_values()
    time_spent = exec_script_on_multiple_threads(method_script)

    print()
    print(method_name)
    print(f"time: {time_spent:.3f} seconds")
    print(f"final row values: {check_table_values()}")


# 4 Methods
def lost_update(conn, cur):
    for _ in range(2000):
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
        conn.commit()

def inplace_update(conn, cur):
    for _ in range(2000):
        cur.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1;")
        conn.commit()

def row_lock(conn, cur):
    for _ in range(2000):
        cur.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        counter = cur.fetchone()[0]
        counter += 1
        cur.execute("UPDATE user_counter SET counter = %s", (counter,))
        conn.commit()

def optimistic_concurrency_ctl(conn, cur):
    for _ in range(2000):
        while True:
            cur.execute("SELECT counter, version FROM user_counter where user_id = 1;")
            counter, version = cur.fetchone()
            counter = counter + 1
            cur.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = 1 AND version = %s;", (counter, version + 1, version))
            conn.commit()
            if cur.rowcount > 0:
                break

if __name__ == "__main__":
    exec_method(method_name="Lost-update", method_script=lost_update)
    exec_method(method_name="In-place update", method_script=inplace_update)
    exec_method(method_name="Row-level locking", method_script=row_lock)
    exec_method(method_name="Optimistic concurrency control", method_script=optimistic_concurrency_ctl)