import os
import json
from typing import List, Dict, Any, Optional
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

class KnowledgeBaseTool:
    def __init__(self, embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        初始化知识库工具
        
        Args:
            embeddings_model: 用于生成文本嵌入的模型名称
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.vectorstore = None
        self.knowledge_base_path = "knowledge_base"
        self.documents_path = os.path.join(self.knowledge_base_path, "documents")
        
        # 创建必要的目录
        os.makedirs(self.documents_path, exist_ok=True)
    
    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加文档到知识库
        
        Args:
            content: 文档内容
            metadata: 文档元数据
        
        Returns:
            bool: 是否添加成功
        """
        try:
            if metadata is None:
                metadata = {}
            
            # 创建Document对象
            document = Document(page_content=content, metadata=metadata)
            
            # 初始化或更新向量存储
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents([document], self.embeddings)
            else:
                self.vectorstore.add_documents([document])
            
            # 保存文档到本地
            doc_id = len(os.listdir(self.documents_path))
            doc_path = os.path.join(self.documents_path, f"doc_{doc_id}.json")
            with open(doc_path, "w", encoding="utf-8") as f:
                json.dump({
                    "content": content,
                    "metadata": metadata
                }, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False
    
    def add_documents_from_directory(self, directory: str) -> int:
        """
        从目录批量添加文档
        
        Args:
            directory: 文档目录路径
        
        Returns:
            int: 添加的文档数量
        """
        added_count = 0
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".txt") or file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        metadata = {
                            "source": file_path,
                            "filename": file
                        }
                        
                        if self.add_document(content, metadata):
                            added_count += 1
                    except Exception as e:
                        print(f"处理文件 {file_path} 失败: {e}")
        
        return added_count
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        """
        搜索知识库
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
        
        Returns:
            List[Document]: 搜索结果
        """
        if self.vectorstore is None:
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def search_with_score(self, query: str, k: int = 3) -> List[tuple[Document, float]]:
        """
        搜索知识库并返回相似度分数
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
        
        Returns:
            List[tuple[Document, float]]: 搜索结果及相似度分数
        """
        if self.vectorstore is None:
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def save(self, path: str = "vectorstore") -> bool:
        """
        保存向量存储
        
        Args:
            path: 保存路径
        
        Returns:
            bool: 是否保存成功
        """
        try:
            if self.vectorstore is not None:
                self.vectorstore.save_local(path)
                return True
            return False
        except Exception as e:
            print(f"保存向量存储失败: {e}")
            return False
    
    def load(self, path: str = "vectorstore") -> bool:
        """
        加载向量存储
        
        Args:
            path: 加载路径
        
        Returns:
            bool: 是否加载成功
        """
        try:
            if os.path.exists(path):
                self.vectorstore = FAISS.load_local(path, self.embeddings)
                return True
            return False
        except Exception as e:
            print(f"加载向量存储失败: {e}")
            return False
    
    def clear(self) -> bool:
        """
        清空知识库
        
        Returns:
            bool: 是否清空成功
        """
        try:
            self.vectorstore = None
            
            # 清空文档目录
            for file in os.listdir(self.documents_path):
                file_path = os.path.join(self.documents_path, file)
                os.remove(file_path)
            
            return True
        except Exception as e:
            print(f"清空知识库失败: {e}")
            return False
    
    def get_document_count(self) -> int:
        """
        获取文档数量
        
        Returns:
            int: 文档数量
        """
        if self.vectorstore is None:
            return 0
        
        try:
            # 注意：FAISS没有直接获取文档数量的方法，这里通过目录文件数量估计
            return len(os.listdir(self.documents_path))
        except Exception as e:
            print(f"获取文档数量失败: {e}")
            return 0

# 测试代码
if __name__ == "__main__":
    kb = KnowledgeBaseTool()
    
    # 添加示例文档
    kb.add_document(
        "辅导员是高校学生思想政治教育和日常管理的骨干力量，主要负责学生的思想政治教育、心理健康教育、就业指导、学生事务管理等工作。",
        {"category": "辅导员职责", "source": "内部资料"}
    )
    
    kb.add_document(
        "学生请假需要填写请假申请表，经辅导员批准后生效。请假天数超过3天的，需要学院领导批准。",
        {"category": "请假流程", "source": "学生手册"}
    )
    
    kb.add_document(
        "心理健康教育中心提供心理咨询服务，学生可以通过预约系统预约心理咨询。",
        {"category": "心理健康", "source": "心理健康教育中心"}
    )
    
    # 测试搜索
    query = "辅导员的职责是什么？"
    results = kb.search(query)
    print(f"搜索结果 ({len(results)}):")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.page_content[:100]}...")
        print(f"   来源: {doc.metadata.get('source', '未知')}")
    
    # 测试搜索带分数
    results_with_score = kb.search_with_score(query)
    print(f"\n带分数的搜索结果:")
    for doc, score in results_with_score:
        print(f"内容: {doc.page_content[:100]}...")
        print(f"分数: {score}")
    
    # 保存和加载
    kb.save()
    print(f"\n文档数量: {kb.get_document_count()}")
