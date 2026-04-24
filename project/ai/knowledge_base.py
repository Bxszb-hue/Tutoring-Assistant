import os
import json
import re
from typing import List, Dict, Any, Optional

class KnowledgeBaseTool:
    def __init__(self, embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        初始化知识库工具
        
        Args:
            embeddings_model: 用于生成文本嵌入的模型名称
        """
        self.embeddings = None
        self.vectorstore = None
        self.knowledge_base_path = "knowledge_base"
        self.documents_path = os.path.join(self.knowledge_base_path, "documents")
        self.documents = []  # 存储文档内容用于关键词搜索
        
        # 创建必要的目录
        os.makedirs(self.documents_path, exist_ok=True)
        
        # 尝试初始化向量存储
        self._initialize_vectorstore()
        
        # 尝试加载现有的向量存储
        if not self.load("vectorstore"):
            # 如果向量存储不存在，尝试从目录加载文档
            self._load_from_directory()
            # 保存向量存储
            self.save("vectorstore")
    
    def _initialize_vectorstore(self):
        """
        初始化向量存储
        """
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            print("Successfully initialized HuggingFace embeddings")
        except Exception as e:
            print(f"Could not initialize HuggingFace embeddings: {str(e)}")
            print("Will use keyword-based search as fallback")
            self.embeddings = None
    
    def _load_from_directory(self):
        """
        从知识库目录加载文档
        """
        print("正在从目录加载知识库文档...")
        
        # 定义需要处理的目录
        directories_to_process = [
            os.path.join(self.knowledge_base_path, "faq"),
            os.path.join(self.knowledge_base_path, "processes"),
            os.path.join(self.knowledge_base_path, "psychological_guidance"),
            os.path.join(self.knowledge_base_path, "regulations")
        ]
        
        total_added = 0
        for directory in directories_to_process:
            if os.path.exists(directory):
                print(f"正在处理目录: {directory}")
                added = self.add_documents_from_directory(directory)
                total_added += added
                print(f"  成功添加 {added} 个文件")
        
        print(f"共添加 {total_added} 个文档到知识库")
    
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
            
            # 存储文档内容用于关键词搜索
            self.documents.append({
                "content": content,
                "metadata": metadata
            })
            
            # 如果有embeddings则创建向量存储
            if self.embeddings is not None:
                try:
                    from langchain_core.documents import Document
                    from langchain_community.vectorstores import FAISS
                    document = Document(page_content=content, metadata=metadata)
                    
                    # 初始化或更新向量存储
                    if self.vectorstore is None:
                        self.vectorstore = FAISS.from_documents([document], self.embeddings)
                    else:
                        self.vectorstore.add_documents([document])
                except ImportError as e:
                    print(f"FAISS not available, skipping vector storage: {e}")
                    # 继续使用关键词搜索
                except Exception as e:
                    print(f"Error creating vector store: {e}")
                    # 继续使用关键词搜索
            
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
                if file.endswith(".txt") or file.endswith(".md") or file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        # 确定文档类型
                        category = "general"
                        if "regulations" in directory:
                            category = "regulation"
                        elif "processes" in directory:
                            category = "process"
                        elif "faq" in directory:
                            category = "faq"
                        
                        metadata = {
                            "source": file_path,
                            "filename": file,
                            "category": category
                        }
                        
                        if self.add_document(content, metadata):
                            added_count += 1
                    except Exception as e:
                        print(f"处理文件 {file_path} 失败: {e}")
        
        return added_count
    
    def add_regulation(self, title: str, content: str, regulation_type: str, 
                      effective_date: str = "", file_number: str = "") -> bool:
        """
        添加规章制度文档
        
        Args:
            title: 规章制度标题
            content: 规章制度内容
            regulation_type: 制度类型（如：违纪处分、奖学金、心理健康等）
            effective_date: 生效日期
            file_number: 文件编号
        
        Returns:
            bool: 是否添加成功
        """
        metadata = {
            "category": "regulation",
            "title": title,
            "regulation_type": regulation_type,
            "effective_date": effective_date,
            "file_number": file_number
        }
        return self.add_document(content, metadata)
    
    def add_process(self, process_name: str, process_steps: List[str], 
                  process_description: str, department: str = "") -> bool:
        """
        添加办事流程文档
        
        Args:
            process_name: 流程名称
            process_steps: 流程步骤列表
            process_description: 流程描述
            department: 负责部门
        
        Returns:
            bool: 是否添加成功
        """
        content = f"{process_name}\n\n{process_description}\n\n办理步骤:\n"
        for i, step in enumerate(process_steps, 1):
            content += f"{i}. {step}\n"
        
        metadata = {
            "category": "process",
            "process_name": process_name,
            "department": department
        }
        return self.add_document(content, metadata)
    
    def add_faq(self, question: str, answer: str, category: str = "general") -> bool:
        """
        添加FAQ文档
        
        Args:
            question: 问题
            answer: 答案
            category: FAQ分类
        
        Returns:
            bool: 是否添加成功
        """
        content = f"Q: {question}\n\nA: {answer}"
        
        metadata = {
            "category": "faq",
            "question": question,
            "faq_category": category
        }
        return self.add_document(content, metadata)
    
    def search_by_category(self, query: str, category: str, k: int = 3) -> List:
        """
        按类别搜索知识库
        
        Args:
            query: 搜索查询
            category: 文档类别
            k: 返回的文档数量
        
        Returns:
            List[Document]: 搜索结果
        """
        all_results = self.search(query, k * 2)
        filtered_results = [doc for doc in all_results if doc.metadata.get("category") == category]
        return filtered_results[:k]
    
    def search(self, query: str, k: int = 3) -> List:
        """
        搜索知识库
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
        
        Returns:
            List: 搜索结果
        """
        # 优先使用向量搜索
        if self.vectorstore is not None and self.embeddings is not None:
            try:
                results = self.vectorstore.similarity_search(query, k=k)
                return results
            except Exception as e:
                print(f"向量搜索失败: {e}")
        
        # 降级到关键词搜索
        return self._keyword_search(query, k)
    
    def _keyword_search(self, query: str, k: int = 3) -> List:
        """
        基于关键词的搜索
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
        
        Returns:
            List: 搜索结果
        """
        print(f"使用关键词搜索: {query}")
        
        if not self.documents:
            return []
        
        # 计算查询词与每个文档的相关性分数
        query_keywords = set(re.findall(r'[\w]+', query.lower()))
        scored_results = []
        
        for doc in self.documents:
            content = doc['content'].lower()
            doc_keywords = set(re.findall(r'[\w]+', content))
            
            # 计算关键词匹配数
            matches = len(query_keywords & doc_keywords)
            
            # 如果有匹配，添加到结果
            if matches > 0:
                # 计算相关性分数（考虑查询词在文档中出现的次数）
                score = matches / len(query_keywords) if query_keywords else 0
                
                # 创建一个类似Document的对象
                class DocResult:
                    def __init__(self, page_content, metadata):
                        self.page_content = page_content
                        self.metadata = metadata
                
                scored_results.append((DocResult(doc['content'], doc['metadata']), score))
        
        # 按分数排序
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前k个结果
        return [doc for doc, score in scored_results[:k]]
    
    def search_with_score(self, query: str, k: int = 3) -> List:
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
            
            # 同时保存文档列表
            docs_path = os.path.join(path, "documents.json")
            os.makedirs(path, exist_ok=True)
            with open(docs_path, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            return True
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
            # 首先加载文档列表
            docs_path = os.path.join(path, "documents.json")
            if os.path.exists(docs_path):
                with open(docs_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
                print(f"加载了 {len(self.documents)} 个文档")
            
            # 尝试加载向量存储
            if os.path.exists(path) and self.embeddings is not None:
                from langchain_community.vectorstores import FAISS
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
        return len(self.documents)

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
