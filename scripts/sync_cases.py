#!/usr/bin/env python3
"""
解析测试脚本并直接写入 MariaDB
支持 pytest 格式的 Python 测试文件
"""
import os
import re
import pymysql
import hashlib
import subprocess
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

def get_modified_files(base_branch='origin/master'):
    """获取修改的 Python 测试文件"""
    try:
        # 获取当前 branch
        current_branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        # 获取修改的文件列表
        result = subprocess.check_output(
            ['git', 'diff', '--name-only', base_branch, 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode()
        
        modified_files = []
        for line in result.split('\n'):
            line = line.strip()
            # 检查是否是 Python 测试文件
            if line and line.endswith('.py') and 'test_' in Path(line).name:
                # 检查文件是否存在
                file_path = Path(line)
                if not file_path.exists():
                    # 尝试绝对路径
                    file_path = Path.cwd() / line
                if file_path.exists():
                    modified_files.append(str(file_path))
                    print(f"Found modified test file: {line}")
        
        return modified_files
    except Exception as e:
        print(f"Warning: Failed to get modified files: {e}")
        return []

def calculate_file_hash(file_path):
    """计算文件内容的 hash 值"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def extract_function_description(content, func_name, search_start=0):
    """提取函数的描述，优先从 pytest.mark.description 提取，其次从 docstring 提取
    Args:
        content: 文件内容
        func_name: 函数名
        search_start: 开始搜索的位置
    Returns:
        函数的描述，如果没有则返回 None
    """
    # 查找函数定义
    pattern = rf'def\s+{re.escape(func_name)}\s*\([^)]*\)\s*:'
    match = re.search(pattern, content[search_start:])
    if not match:
        return None
    
    # 获取函数定义的起始位置
    func_def_start = search_start + match.start()
    
    # 查找函数定义之前的 pytest mark（包括 description）
    # 回溯查找，最多回溯 500 个字符
    lookback_start = max(0, func_def_start - 500)
    lines_before = content[lookback_start:func_def_start]
    
    # 查找 @pytest.mark.description('...')
    desc_pattern = r'@pytest\.mark\.description\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
    desc_match = re.search(desc_pattern, lines_before)
    if desc_match:
        return desc_match.group(1).strip()[:500]
    
    # 如果没有找到 pytest.mark.description，提取 docstring
    func_start = search_start + match.end()
    
    # 查找第一个 docstring（单引号或双引号）
    docstring_pattern = r'''(?:\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?"""|\'[^\']*\'|"[^"]*")'''
    docstring_match = re.search(docstring_pattern, content[func_start:], re.MULTILINE | re.DOTALL)
    
    if docstring_match:
        docstring = docstring_match.group(0).strip()
        # 移除引号
        if (docstring.startswith("'''") and docstring.endswith("'''")) or \
           (docstring.startswith('"""') and docstring.endswith('"""')):
            docstring = docstring[3:-3]
        elif (docstring.startswith("'") and docstring.endswith("'")) or \
             (docstring.startswith('"') and docstring.endswith('"')):
            docstring = docstring[1:-1]
        
        # 清理空白
        docstring = ' '.join(line.strip() for line in docstring.split('\n') if line.strip())
        return docstring[:500] if docstring else None  # 限制长度
    
    return None

def parse_test_files(test_dir=None, modified_files=None):
    """解析所有 Python 测试文件
    Args:
        test_dir: 测试目录，如果为 None 则从环境变量读取或使用默认值
        modified_files: 只解析这些文件，如果为 None 则解析所有文件
    """
    cases = []
    
    # 如果没有指定目录，从环境变量读取或使用默认值
    if test_dir is None:
        test_dir = os.environ.get('TEST_DIR', 'examples')
    
    test_path = Path(test_dir)
    
    # 如果指定了修改的文件，转换为 Path 对象
    if modified_files is not None:
        file_set = {Path(f) for f in modified_files}
        print(f"Only syncing modified files: {len(file_set)} files")
    else:
        file_set = None

    if not test_path.exists():
        print(f"Warning: Test directory '{test_dir}' not found")
        return cases

    for py_file in test_path.rglob('test_*.py'):
        # 如果指定了修改的文件，只解析那些文件
        if file_set is not None:
            # 检查文件是否在修改列表中
            found = False
            py_file_str = str(py_file.resolve())
            py_file_rel = str(py_file)
            for modified_file in file_set:
                try:
                    modified_str = str(modified_file.resolve())
                    modified_rel = str(modified_file)
                    # 检查是否匹配（处理绝对路径和相对路径）
                    if (modified_str == py_file_str or 
                        modified_rel == py_file_rel or
                        py_file_str.endswith(modified_str) or
                        py_file_str.endswith(modified_rel)):
                        found = True
                        break
                except Exception:
                    continue
            if not found:
                continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
            continue

        rel_path = str(py_file).replace('\\', '/')

        # 推断用例类型
        case_type = 'ui' if 'ui' in rel_path.lower() else 'api'

        # 匹配 class TestXxx 和 def test_xxx
        class_pattern = r'class\s+(Test\w+)\s*(?:\([^)]*\))?\s*:'
        method_pattern = r'def\s+(test_\w+)\s*\([^)]*\)'

        # 解析类和方法
        for class_match in re.finditer(class_pattern, content):
            class_name = class_match.group(1)
            class_start = class_match.end()

            # 查找下一个类或文件末尾
            next_class = re.search(class_pattern, content[class_start:])
            class_end = class_start + next_class.start() if next_class else len(content)
            class_content = content[class_start:class_end]

            for method_match in re.finditer(method_pattern, class_content):
                method_name = method_match.group(1)

                # 构建 pytest 格式的脚本路径
                script_path = f'{rel_path}::{class_name}::{method_name}'
                
                # 提取方法的描述
                method_start = class_start + method_match.start()
                description = extract_function_description(content, method_name, method_start)

                cases.append({
                    'name': f'{class_name}::{method_name}',
                    'module': class_name,
                    'type': case_type,
                    'priority': 'P1',
                    'script_path': script_path,
                    'tags': 'auto-synced,gitee',
                    'description': description
                })

        # 解析独立的 test_ 函数（不在类内）
        # 首先移除所有类的内容
        content_no_class = re.sub(
            r'class\s+Test\w+\s*(?:\([^)]*\))?\s*:.*?(?=\nclass\s|\Z)',
            '',
            content,
            flags=re.DOTALL
        )

        for func_match in re.finditer(method_pattern, content_no_class):
            func_name = func_match.group(1)
            script_path = f'{rel_path}::{func_name}'
            
            # 提取函数的描述
            func_start = func_match.start()
            description = extract_function_description(content, func_name, func_start)

            cases.append({
                'name': func_name,
                'module': None,
                'type': case_type,
                'priority': 'P1',
                'script_path': script_path,
                'tags': 'auto-synced,gitee',
                'description': description
            })

    return cases

def get_current_commit_hash():
    """获取当前 commit hash"""
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None

def case_has_changes(cursor, case, new_commit_hash):
    """检查用例是否有变化
    Returns: (has_changes, existing_case)
    """
    case_key = case['script_path']
    
    # 查询现有记录
    cursor.execute(
        "SELECT * FROM Auto_TestCase WHERE case_key = %s",
        (case_key,)
    )
    existing = cursor.fetchone()
    
    if not existing:
        return True, None  # 新用例
    
    # 检查 commit hash 是否相同
    if existing.get('last_sync_commit') == new_commit_hash:
        # commit hash 相同，检查其他字段是否有变化
        if (existing.get('name') == case['name'] and
            existing.get('module') == case['module'] and
            existing.get('priority') == case['priority'] and
            existing.get('tags') == case['tags'] and
            existing.get('type') == case['type'] and
            existing.get('description') == case.get('description')):
            return False, existing  # 无变化
    
    return True, existing  # 有变化

def sync_to_db(cases):
    """同步用例到数据库"""
    if not cases:
        print('No cases to sync')
        return

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            synced = 0
            skipped = 0
            # 获取当前 commit hash
            commit_hash = get_current_commit_hash()
            print(f"Current commit: {commit_hash[:8] if commit_hash else 'unknown'}")
            
            # repo_id 从环境变量获取，默认为 1
            repo_id = int(os.environ.get('REPO_ID', '1'))

            for case in cases:
                case_key = case['script_path']
                
                # 检查是否有变化
                has_changes, existing_case = case_has_changes(cursor, case, commit_hash)
                
                if not has_changes:
                    skipped += 1
                    continue
                
                # 存在则更新，不存在则插入
                sql = """
                    INSERT INTO Auto_TestCase
                        (case_key, name, module, priority, script_path, tags, type, source, enabled, repo_id, last_sync_commit, description)
                    VALUES
                        (%(case_key)s, %(name)s, %(module)s, %(priority)s, %(script_path)s, %(tags)s, %(type)s, 'git', 1, %(repo_id)s, %(commit_hash)s, %(description)s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        module = VALUES(module),
                        type = VALUES(type),
                        tags = VALUES(tags),
                        description = VALUES(description),
                        last_sync_commit = VALUES(last_sync_commit),
                        updated_at = NOW()
                """
                try:
                    cursor.execute(sql, {
                        'case_key': case_key,
                        'name': case['name'],
                        'module': case['module'],
                        'priority': case['priority'],
                        'script_path': case['script_path'],
                        'tags': case['tags'],
                        'type': case['type'],
                        'repo_id': repo_id,
                        'commit_hash': commit_hash,
                        'description': case.get('description')
                    })
                    synced += 1
                except Exception as e:
                    print(f"Error syncing case {case['name']}: {e}")

            conn.commit()
            print(f'Successfully synced {synced}/{len(cases)} cases, skipped {skipped} unchanged cases')

    finally:
        conn.close()

def main():
    """主函数"""
    print('Starting test case sync...')
    print(f'Repository: {os.environ.get("GITHUB_REPOSITORY", "unknown")}')
    print(f'Branch: {os.environ.get("GITHUB_REF_NAME", "unknown")}')

    # 检查是否是增量同步（默认为增量同步）
    force_sync = os.environ.get('FORCE_SYNC', 'false').lower() == 'true'
    trigger_type = os.environ.get('TRIGGER_TYPE', 'unknown')
    
    if force_sync or trigger_type == 'schedule':
        # 强制同步或定时任务，扫描所有文件
        print('Force sync enabled or scheduled job, scanning all files...')
        cases = parse_test_files()
    else:
        # 增量同步，只扫描修改的文件
        print('Incremental sync, only scanning modified files...')
        modified_files = get_modified_files()
        if modified_files:
            print(f'Found {len(modified_files)} modified test files')
            cases = parse_test_files(modified_files=modified_files)
        else:
            print('No modified test files found')
            # 如果没有修改的文件，不进行同步
            return
    
    print(f'Found {len(cases)} test cases to sync')

    if cases:
        sync_to_db(cases)
    else:
        print('No test cases found to sync')

if __name__ == '__main__':
    main()
