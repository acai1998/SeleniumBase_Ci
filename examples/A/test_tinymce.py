from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class TinyMceTest#!/usr/bin/env python3
"""调试脚本：模拟 sync_cases.py 的解析逻辑，打印每个文件的解析结果"""
import re
import os
import sys
from pathlib import Path

sys.path.insert(0, '/Users/wb_caijinwei/SeleniumBase_Ci/scripts')

# 直接复制 parse_test_files 的逻辑来调试
test_dir = 'examples'
test_path = Path(test_dir)
os.chdir('/Users/wb_caijinwei/SeleniumBase_Ci')

class_pattern = r'class\s+(\w+)\s*(?:\([^)]*\))?\s*:'
method_pattern = r'def\s+(test_\w+)\s*\([^)]*\)'

test_files = sorted(set(test_path.rglob('test_*.py')) | set(test_path.rglob('*_test.py')))
print(f"找到测试文件: {len(test_files)} 个\n")

total_cases = 0
file_stats = []

for py_file in test_files:
    content = py_file.read_text(encoding='utf-8')
    rel_path = str(py_file).replace('\\', '/')

    class_cases = []
    # 解析类内方法
    for class_match in re.finditer(class_pattern, content):
        class_name = class_match.group(1)
        class_start = class_match.end()
        next_class = re.search(class_pattern, content[class_start:])
        class_end = class_start + next_class.start() if next_class else len(content)
        class_content = content[class_start:class_end]
        methods = re.findall(method_pattern, class_content)
        for m in methods:
            class_cases.append(f"{class_name}::{m}")

    # 解析独立函数（新逻辑）
    top_level_lines = []
    inside_class = False
    for line in content.split('\n'):
        if re.match(r'^class\s+\w+', line):
            inside_class = True
            continue
        if inside_class and line and not line[0].isspace() and not line.startswith('#'):
            inside_class = False
        if not inside_class:
            top_level_lines.append(line)
    content_no_class = '\n'.join(top_level_lines)
    func_cases = re.findall(method_pattern, content_no_class)

    all_cases = class_cases + func_cases
    file_stats.append((rel_path, len(all_cases), class_cases, func_cases))
    total_cases += len(all_cases)

    if len(all_cases) == 0:
        # 直接 grep 一下文件里有没有 def test_
        raw_methods = re.findall(method_pattern, content)
        print(f"⚠️  {rel_path}: 0 条 (但文件里有 {len(raw_methods)} 个 test_ 方法: {raw_methods})")
    else:
        print(f"✅ {rel_path}: {len(all_cases)} 条")

print(f"\n=== 汇总 ===")
print(f"文件总数: {len(test_files)}")
print(f"解析用例总数: {total_cases}")
print(f"\n=== 0条文件详情 ===")
for path, count, cls, fn in file_stats:
    if count == 0:
        content = Path(path).read_text()
        raw = re.findall(method_pattern, content)
        class_names = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        print(f"  {path}")
        print(f"    类名: {class_names}, 原始test方法: {raw}")
(BaseCase):
    @pytest.mark.owner('wubin')
    @pytest.mark.priority('P3')
    @pytest.mark.description('验证 TinyMCE 富文本编辑器的功能')
    def test_tinymce(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            self.skip("Skip this test in headless mode!")
        self.open("https://seleniumbase.io/tinymce/")
        self.wait_for_element("div.mce-container-body")
        self.click('span:contains("File")')
        self.click('span:contains("New document")')
        self.click('span:contains("Paragraph")')
        self.click('span:contains("Heading 2")')
        self.switch_to_frame("iframe")
        self.add_text("#tinymce", "Automate anything with SeleniumBase!\n")
        self.switch_to_parent_frame()
        self.click("button i.mce-i-image")
        self.type('input[aria-label="Width"].mce-textbox', "300")
        image_url = "https://seleniumbase.github.io/img/sb_logo_10.png"
        self.type("input.mce-textbox", image_url + "\n")
        with self.frame_switch("iframe"):
            self.click("h2")
            self.post_message("Automate anything with SeleniumBase!")
        self.click('span:contains("File")')
        self.click('span:contains("Preview")')
        self.switch_to_frame('iframe[sandbox="allow-scripts"]')
        self.post_message("Learn SeleniumBase Today!")
