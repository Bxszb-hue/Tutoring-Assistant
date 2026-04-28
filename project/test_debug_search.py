import sys
import re
sys.path.insert(0, '.')

from ai.knowledge_base import KnowledgeBaseTool

print("初始化知识库...")
kb = KnowledgeBaseTool()

print(f"\n知识库中共有 {kb.get_document_count()} 个文档")

# 查找包含"请假"的文档
print("\n查找包含'请假'的文档:")
query = "请假流程"
query_keywords = set(re.findall(r'[\w\u4e00-\u9fa5]+', query.lower()))
print(f"查询关键词: {query_keywords}")

found_count = 0
for i, doc in enumerate(kb.documents):
    content = doc['content'].lower()
    doc_keywords = set(re.findall(r'[\w\u4e00-\u9fa5]+', content))
    matches = query_keywords & doc_keywords
    if '请假' in content:
        found_count += 1
        print(f"\n文档 {i}: {doc['metadata'].get('filename', 'unknown')}")
        print(f"  包含'请假': 是")
        print(f"  文档关键词数: {len(doc_keywords)}")
        print(f"  匹配数: {len(matches)}")
        print(f"  匹配关键词: {matches}")
        if found_count >= 3:
            break

print(f"\n总共找到 {found_count} 个包含'请假'的文档")

# 检查学生请假办理流程.md的内容
print("\n检查'学生请假办理流程.md'的内容:")
for doc in kb.documents:
    if doc['metadata'].get('filename') == '学生请假办理流程.md':
        print(f"内容前200字: {doc['content'][:200]}")
        content = doc['content'].lower()
        doc_keywords = set(re.findall(r'[\w\u4e00-\u9fa5]+', content))
        print(f"文档关键词: {doc_keywords}")
        matches = query_keywords & doc_keywords
        print(f"与查询'{query}'的匹配: {matches}")
        break