#!/usr/bin/env python3
"""
初始化知识库脚本

该脚本用于加载现有的知识库文件到向量存储中
"""

import os
import sys
from ai.knowledge_base import KnowledgeBaseTool

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def initialize_knowledge_base():
    """
    初始化知识库，加载现有的知识库文件
    """
    print("正在初始化知识库...")
    
    # 创建知识库工具实例
    kb = KnowledgeBaseTool()
    
    # 定义知识库目录
    knowledge_base_dir = "knowledge_base"
    
    # 检查知识库目录是否存在
    if not os.path.exists(knowledge_base_dir):
        print(f"错误：知识库目录 {knowledge_base_dir} 不存在")
        return False
    
    # 遍历知识库目录下的所有文件
    total_added = 0
    
    # 定义需要处理的目录
    directories_to_process = [
        os.path.join(knowledge_base_dir, "faq"),
        os.path.join(knowledge_base_dir, "processes"),
        os.path.join(knowledge_base_dir, "psychological_guidance"),
        os.path.join(knowledge_base_dir, "regulations")
    ]
    
    for directory in directories_to_process:
        if os.path.exists(directory):
            print(f"正在处理目录: {directory}")
            added = kb.add_documents_from_directory(directory)
            total_added += added
            print(f"  成功添加 {added} 个文件")
    
    # 保存向量存储
    if kb.save("vectorstore"):
        print(f"成功保存向量存储，共添加 {total_added} 个文档")
        print(f"知识库初始化完成，当前文档数量: {kb.get_document_count()}")
        return True
    else:
        print("保存向量存储失败")
        return False

def test_knowledge_base():
    """
    测试知识库功能
    """
    print("\n测试知识库功能...")
    
    kb = KnowledgeBaseTool()
    
    # 测试搜索
    test_queries = [
        "如何申请奖学金？",
        "请假流程是什么？",
        "如何应对学习压力？",
        "宿舍报修流程"
    ]
    
    for query in test_queries:
        print(f"\n测试查询: {query}")
        results = kb.search(query, k=2)
        print(f"  找到 {len(results)} 个结果")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.page_content[:100]}...")
            print(f"    来源: {result.metadata.get('source', '未知')}")

if __name__ == "__main__":
    if initialize_knowledge_base():
        test_knowledge_base()
    else:
        print("知识库初始化失败")
