#!/usr/bin/env python3
"""
简化版知识库工具 - 不依赖外部模型
适用于演示和测试
"""
import os
import json
from typing import List, Dict, Any, Optional

class SimpleDocument:
    """简化文档类"""
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.page_content = content
        self.metadata = metadata or {}

class SimpleKnowledgeBaseTool:
    """简化版知识库工具"""
    def __init__(self):
        self.documents: List[SimpleDocument] = []
        self.knowledge_base_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
        
        # 创建必要的目录
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_path, "regulations"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_path, "processes"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_path, "faq"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_path, "psychological_guidance"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_path, "documents"), exist_ok=True)
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> bool:
        """添加文档"""
        try:
            doc = SimpleDocument(content, metadata)
            self.documents.append(doc)
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
    
    def add_regulation(self, title: str, content: str, regulation_type: str, 
                      effective_date: str = "", file_number: str = "") -> bool:
        """添加规章制度文档"""
        metadata = {
            "category": "regulation",
            "title": title,
            "regulation_type": regulation_type,
            "effective_date": effective_date,
            "file_number": file_number
        }
        
        # 保存到文件
        filename = f"{regulation_type}_{title}.md"
        filepath = os.path.join(self.knowledge_base_path, "regulations", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"## 基本信息\n\n")
            f.write(f"- 文件编号: {file_number}\n")
            f.write(f"- 生效日期: {effective_date}\n")
            f.write(f"- 制度类型: {regulation_type}\n\n")
            f.write(f"## 内容\n\n{content}\n")
        
        return self.add_document(content, metadata)
    
    def add_process(self, process_name: str, process_steps: List[str], 
                  process_description: str, department: str = "") -> bool:
        """添加办事流程文档"""
        content = f"{process_name}\n\n{process_description}\n\n办理步骤:\n"
        for i, step in enumerate(process_steps, 1):
            content += f"{i}. {step}\n"
        
        metadata = {
            "category": "process",
            "process_name": process_name,
            "department": department
        }
        
        # 保存到文件
        filename = f"{process_name}.md"
        filepath = os.path.join(self.knowledge_base_path, "processes", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {process_name}\n\n")
            f.write(f"## 描述\n\n{process_description}\n\n")
            f.write(f"## 负责部门\n\n{department}\n\n")
            f.write(f"## 办理步骤\n\n")
            for i, step in enumerate(process_steps, 1):
                f.write(f"{i}. {step}\n")
        
        return self.add_document(content, metadata)
    
    def add_faq(self, question: str, answer: str, category: str = "general") -> bool:
        """添加FAQ文档"""
        content = f"Q: {question}\n\nA: {answer}"
        
        metadata = {
            "category": "faq",
            "question": question,
            "faq_category": category
        }
        
        # 保存到文件
        filename = f"faq_{category}_{len(self.documents)}.md"
        filepath = os.path.join(self.knowledge_base_path, "faq", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# FAQ - {question}\n\n")
            f.write(f"## 分类\n\n{category}\n\n")
            f.write(f"## 问题\n\n{question}\n\n")
            f.write(f"## 答案\n\n{answer}\n")
        
        return self.add_document(content, metadata)
    
    def add_psychological_guidance(self, title: str, content: str, 
                                  guidance_type: str, suitable_for: str = "", 
                                  mood_type: str = "") -> bool:
        """添加心理导言文档"""
        metadata = {
            "category": "psychological_guidance",
            "title": title,
            "guidance_type": guidance_type,
            "suitable_for": suitable_for,
            "mood_type": mood_type
        }
        
        # 保存到文件
        filename = f"{guidance_type}_{title}.md"
        filepath = os.path.join(self.knowledge_base_path, "psychological_guidance", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"## 导言类型\n\n{guidance_type}\n\n")
            f.write(f"## 适用人群\n\n{suitable_for}\n\n")
            f.write(f"## 情绪类型\n\n{mood_type}\n\n")
            f.write(f"## 导言内容\n\n{content}\n")
        
        return self.add_document(content, metadata)
    
    def search(self, query: str, k: int = 3) -> List[SimpleDocument]:
        """简化的搜索功能 - 基于关键词匹配"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            # 简单的关键词匹配
            content_lower = doc.page_content.lower()
            if query_lower in content_lower:
                results.append(doc)
            elif doc.metadata.get("question"):
                if query_lower in doc.metadata["question"].lower():
                    results.append(doc)
        
        # 按相关程度排序（简单的匹配度）
        results.sort(key=lambda x: x.page_content.lower().count(query_lower), reverse=True)
        
        return results[:k]
    
    def search_by_category(self, query: str, category: str, k: int = 3) -> List[SimpleDocument]:
        """按类别搜索"""
        all_results = self.search(query, k * 2)
        filtered_results = [doc for doc in all_results if doc.metadata.get("category") == category]
        return filtered_results[:k]
    
    def save(self, save_path: str = None) -> bool:
        """保存知识库（这里主要保存元数据）"""
        try:
            if not save_path:
                save_path = os.path.join(self.knowledge_base_path, "vector_store")
            
            os.makedirs(save_path, exist_ok=True)
            
            # 保存文档元数据
            metadata_list = []
            for i, doc in enumerate(self.documents):
                metadata_list.append({
                    "index": i,
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                })
            
            with open(os.path.join(save_path, "knowledge_base_metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata_list, f, ensure_ascii=False, indent=2)
            
            # 保存完整知识库内容
            with open(os.path.join(save_path, "knowledge_base_full.json"), "w", encoding="utf-8") as f:
                full_data = []
                for doc in self.documents:
                    full_data.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    })
                json.dump(full_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存知识库失败: {e}")
            return False
    
    def load(self, load_path: str = None) -> bool:
        """加载知识库"""
        try:
            if not load_path:
                load_path = os.path.join(self.knowledge_base_path, "vector_store")
            
            metadata_file = os.path.join(load_path, "knowledge_base_full.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.documents = []
                for item in data:
                    doc = SimpleDocument(item["content"], item["metadata"])
                    self.documents.append(doc)
                
                return True
            return False
        except Exception as e:
            print(f"加载知识库失败: {e}")
            return False
