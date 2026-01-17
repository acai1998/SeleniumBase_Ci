#!/usr/bin/env python3
"""
解析测试脚本并直接写入 MariaDB
支持 pytest 格式的 Python 测试文件
"""
import os
import re
import pymysql
from pathlib import Path


def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def extract_metadata(content: str, func_start: int) -> dict:
    """
    提取函数上方的元数据
    支持两种格式：
        1. 注释格式：# @owner: zhangsan
        2. 装饰器格式：@pytest.mark.owner('zhangsan')
    """
    metadata = {
        'owner': None,
        'priority': 'P1',
        'description': None
    }
    
    # 向上查找（最多 500 个字符）
    search_start = max(0, func_start - 500)
    before_func = content[search_start:func_start]
    
    # ========== 装饰器格式 ==========
    # @pytest.mark.owner('caijinwei') 或 @pytest.mark.owner("caijinwei")
    owner_match = re.search(r'@pytest\.mark\.owner\([\'"](.+?)[\'"]\)', before_func)
    if owner_match:
        metadata['owner'] = owner_match.group(1)
    
    # @pytest.mark.priority('P0')
    priority_match = re.search(r'@pytest\.mark\.priority\([\'"](.+?)[\'"]\)', before_func)
    if priority_match:
        metadata['priority'] = priority_match.group(1).upper()
    
    # @pytest.mark.description('登录用例')
    desc_match = re.search(r'@pytest\.mark\.description\([\'"](.+?)[\'"]\)', before_func)
    if desc_match:
        metadata['description'] = desc_match.group(1)
    
    # ========== 注释格式（兼容） ==========
    if not metadata['owner']:
        owner_match = re.search(r'#\s*@owner:\s*(\S+)', before_func)
        if owner_match:
            metadata['owner'] = owner_match.group(1)
    
    if metadata['priority'] == 'P1':  # 没被装饰器覆盖才用注释
        priority_match = re.search(r'#\s*@priority:\s*(P[0-3])', before_func, re.IGNORECASE)
        if priority_match:
            metadata['priority'] = priority_match.group(1).upper()
    
    if not metadata['description']:
        desc_match = re.search(r'#\s*@description:\s*(.+?)(?:\n|$)', before_func)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()
    
    return metadata



def parse_test_files():
    """解析测试文件并提取用例信息"""
    cases = []
    examples_dir = Path('examples')
    
    if not examples_dir.exists():
        print(f'Warning: {examples_dir} directory not found')
        return cases
    
    # 查找所有测试文件
    test_files = list(examples_dir.glob('test_*.py')) + list(examples_dir.glob('*_test.py'))
    
    for file_path in test_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有 test_ 开头的函数
            pattern = r'def\s+(test_\w+)\s*\('
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                func_start = match.start()
                
                # 提取元数据
                metadata = extract_metadata(content, func_start)
                
                # 构建用例信息
                case = {
                    'name': func_name,
                    'module': file_path.stem,  # 文件名(不含扩展名)
                    'type': '1',  # 类型代码(根据数据库定义)
                    'priority': metadata.get('priority', 'P1'),
                    'owner': metadata.get('owner'),  # 负责人
                    'description': metadata.get('description'),  # 描述
                    'script_path': str(file_path.relative_to('.')).replace('\\', '/'),
                    'tags': ''  # 预留给其他标签
                }
                
                cases.append(case)
                
        except Exception as e:
            print(f'Error parsing {file_path}: {e}')
            continue
    
    return cases


def sync_to_db(cases):
    """同步用例到数据库"""
    if not cases:
        print('No cases to sync')
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            synced = 0
            for case in cases:
                # 使用 script_path 作为唯一标识
                # 存在则更新，不存在则插入
                sql = """
                     INSERT INTO Auto_TestCase
                            (case_key, name, module, type, priority, owner, description, script_path, tags, repo_id, source, enabled)
                        VALUES
                            (%(name)s, %(name)s, %(module)s, %(type)s, %(priority)s, %(owner)s, %(description)s, %(script_path)s, %(tags)s, 1, 'git', 1)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            module = VALUES(module),
                            type = VALUES(type),
                            priority = VALUES(priority),
                            owner = VALUES(owner),
                            description = VALUES(description),
                            tags = VALUES(tags),
                            enabled = 1,
                            updated_at = NOW()
                """
                try:
                    # 打印调试信息
                    print(f"Syncing case: {case['name']}, type={case['type']}, len={len(case['type'])}")
                    cursor.execute(sql, case)
                    synced += 1
                except Exception as e:
                    print(f"Error syncing case {case['name']}: {e}")
                    print(f"Case data: {case}")

            conn.commit()
            print(f'Successfully synced {synced}/{len(cases)} cases')

    finally:
        conn.close()


def main():
    """主函数"""
    print('Starting test case sync...')
    print(f'Repository: {os.environ.get("GITHUB_REPOSITORY", "unknown")}')
    print(f'Branch: {os.environ.get("GITHUB_REF_NAME", "unknown")}')

    cases = parse_test_files()
    print(f'Found {len(cases)} test cases')

    if cases:
        sync_to_db(cases)
    else:
        print('No test cases found to sync')


if __name__ == '__main__':
    main()