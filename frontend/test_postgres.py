import os
import sys
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_URL = os.getenv('POSTGRES_URL')
if not POSTGRES_URL:
    print('POSTGRES_URL not found in .env')
    sys.exit(1)

try:
    conn = psycopg2.connect(POSTGRES_URL)
    cur = conn.cursor()
    # 如果 User 表不存在则创建
    cur.execute('''
        CREATE TABLE IF NOT EXISTS "User" (
            "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
            "email" varchar(64) NOT NULL,
            "password" varchar(64)
        );
    ''')
    conn.commit()
    # 测试插入到用户表
    cur.execute("INSERT INTO \"User\" (email, password) VALUES (%s, %s)", ('test@example.com', 'testpassword'))
    conn.commit()
    print('插入成功！')
    cur.execute("DELETE FROM \"User\" WHERE email = 'test@example.com'")
    conn.commit()
    print('测试数据已删除。')
except Exception as e:
    print(f'操作失败: {e}')
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()