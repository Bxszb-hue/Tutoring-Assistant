#!/usr/bin/env python3
"""
知识库API服务
提供知识库的查询、更新和管理接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ai.knowledge_base_simple import SimpleKnowledgeBaseTool

router = APIRouter(prefix="/knowledge", tags=["知识库"])

# 全局知识库实例
_knowledge_base = None

def get_knowledge_base() -> SimpleKnowledgeBaseTool:
    """获取知识库实例"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = SimpleKnowledgeBaseTool()
        try:
            _knowledge_base.load()
        except:
            pass
    return _knowledge_base

class SearchRequest(BaseModel):
    query: str
    k: int = 3
    category: Optional[str] = None

class DocumentInfo(BaseModel):
    content: str
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    results: List[DocumentInfo]
    total: int

class AddRegulationRequest(BaseModel):
    title: str
    content: str
    regulation_type: str
    effective_date: str = ""
    file_number: str = ""

class AddProcessRequest(BaseModel):
    process_name: str
    process_steps: List[str]
    process_description: str
    department: str = ""

class AddFAQRequest(BaseModel):
    question: str
    answer: str
    category: str = "general"

class AddPsychologicalGuidanceRequest(BaseModel):
    title: str
    content: str
    guidance_type: str
    suitable_for: str = ""
    mood_type: str = ""

@router.post("/search", response_model=SearchResponse)
async def search_knowledge(request: SearchRequest):
    """搜索知识库"""
    try:
        kb = get_knowledge_base()
        
        if request.category:
            results = kb.search_by_category(request.query, request.category, k=request.k)
        else:
            results = kb.search(request.query, k=request.k)
        
        documents = []
        for doc in results:
            documents.append(DocumentInfo(
                content=doc.page_content,
                metadata=doc.metadata
            ))
        
        return SearchResponse(
            results=documents,
            total=len(documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    """获取知识库分类"""
    return {
        "categories": [
            {
                "id": "regulation",
                "name": "规章制度",
                "description": "学校各类规章制度文件"
            },
            {
                "id": "process",
                "name": "办事流程",
                "description": "各类事务办理流程"
            },
            {
                "id": "faq",
                "name": "常见问题",
                "description": "常见问题解答"
            },
            {
                "id": "psychological_guidance",
                "name": "心理导言",
                "description": "心理关怀导言内容"
            }
        ]
    }

@router.post("/regulations/add")
async def add_regulation(request: AddRegulationRequest):
    """添加规章制度"""
    try:
        kb = get_knowledge_base()
        success = kb.add_regulation(
            title=request.title,
            content=request.content,
            regulation_type=request.regulation_type,
            effective_date=request.effective_date,
            file_number=request.file_number
        )
        
        if success:
            # 保存知识库
            kb.save()
            return {"success": True, "message": "规章制度添加成功"}
        else:
            raise HTTPException(status_code=500, detail="添加失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/processes/add")
async def add_process(request: AddProcessRequest):
    """添加办事流程"""
    try:
        kb = get_knowledge_base()
        success = kb.add_process(
            process_name=request.process_name,
            process_steps=request.process_steps,
            process_description=request.process_description,
            department=request.department
        )
        
        if success:
            kb.save()
            return {"success": True, "message": "办事流程添加成功"}
        else:
            raise HTTPException(status_code=500, detail="添加失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/faq/add")
async def add_faq(request: AddFAQRequest):
    """添加FAQ"""
    try:
        kb = get_knowledge_base()
        success = kb.add_faq(
            question=request.question,
            answer=request.answer,
            category=request.category
        )
        
        if success:
            kb.save()
            return {"success": True, "message": "FAQ添加成功"}
        else:
            raise HTTPException(status_code=500, detail="添加失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/psychological_guidance/add")
async def add_psychological_guidance(request: AddPsychologicalGuidanceRequest):
    """添加心理导言"""
    try:
        kb = get_knowledge_base()
        success = kb.add_psychological_guidance(
            title=request.title,
            content=request.content,
            guidance_type=request.guidance_type,
            suitable_for=request.suitable_for,
            mood_type=request.mood_type
        )
        
        if success:
            kb.save()
            return {"success": True, "message": "心理导言添加成功"}
        else:
            raise HTTPException(status_code=500, detail="添加失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_knowledge_stats():
    """获取知识库统计信息"""
    try:
        kb = get_knowledge_base()
        
        # 统计各类文档数量
        stats = {
            "total_documents": len(kb.documents),
            "categories": {
                "regulation": 0,
                "process": 0,
                "faq": 0,
                "psychological_guidance": 0
            }
        }
        
        for doc in kb.documents:
            category = doc.metadata.get("category")
            if category in stats["categories"]:
                stats["categories"][category] += 1
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
