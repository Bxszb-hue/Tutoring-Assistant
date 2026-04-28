import sys
sys.path.insert(0, '.')

from ai.knowledge_base import KnowledgeBaseTool

print("初始化知识库...")
kb = KnowledgeBaseTool()

print(f"\n知识库中共有 {kb.get_document_count()} 个文档")

print("\n测试搜索：请假流程")
results = kb.search("请假流程", k=3)
print(f"找到 {len(results)} 个结果")

if results:
    for i, r in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(f"内容: {r.page_content[:200]}...")
else:
    print("没有找到结果！")

print("\n测试搜索：奖学金")
results2 = kb.search("奖学金", k=3)
print(f"找到 {len(results2)} 个结果")

if results2:
    for i, r in enumerate(results2):
        print(f"\n结果 {i+1}:")
        print(f"内容: {r.page_content[:200]}...")