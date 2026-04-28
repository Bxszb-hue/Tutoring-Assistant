import sys
sys.path.insert(0, '.')

from ai.knowledge_base import KnowledgeBaseTool

print("初始化知识库...")
kb = KnowledgeBaseTool()

print(f"\n知识库中共有 {kb.get_document_count()} 个文档")

# 测试不同的查询
test_queries = [
    "请假流程",
    "请假流程是什么？",
    "奖学金",
    "奖学金怎么获得？"
]

for query in test_queries:
    print(f"\n{'='*50}")
    print(f"测试搜索：{query}")
    results = kb.search(query, k=3)
    print(f"找到 {len(results)} 个结果")
    
    if results:
        for i, r in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(f"内容: {r.page_content[:150]}...")