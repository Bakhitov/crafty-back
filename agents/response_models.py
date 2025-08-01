"""
Реестр Pydantic моделей для Response Model динамических агентов.
Позволяет использовать модели по имени в JSON конфигурациях.
"""

from typing import Dict, Type, Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# === ГОТОВЫЕ RESPONSE MODELS ===

class TaskStatus(str, Enum):
    """Статус выполнения задачи"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResult(BaseModel):
    """Результат выполнения задачи"""
    success: bool = Field(description="Успешно ли выполнена задача")
    message: str = Field(description="Сообщение о результате")
    status: TaskStatus = Field(description="Статус задачи")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные данные")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Время выполнения")


class UserAnalysis(BaseModel):
    """Анализ пользователя"""
    name: str = Field(description="Имя пользователя")
    age: Optional[int] = Field(default=None, description="Возраст пользователя")
    interests: List[str] = Field(default=[], description="Интересы пользователя")
    sentiment: str = Field(description="Эмоциональная оценка (positive/negative/neutral)")
    confidence: float = Field(ge=0.0, le=1.0, description="Уверенность в анализе")


class SearchResult(BaseModel):
    """Результат поиска"""
    query: str = Field(description="Поисковый запрос")
    results: List[Dict[str, Any]] = Field(description="Найденные результаты")
    total_count: int = Field(ge=0, description="Общее количество результатов")
    search_time: float = Field(description="Время поиска в секундах")
    page: int = Field(default=1, ge=1, description="Номер страницы")


class DocumentSummary(BaseModel):
    """Краткое содержание документа"""
    title: str = Field(description="Заголовок документа")
    summary: str = Field(description="Краткое содержание")
    key_points: List[str] = Field(description="Ключевые моменты")
    word_count: int = Field(ge=0, description="Количество слов")
    reading_time_minutes: int = Field(ge=0, description="Время чтения в минутах")
    language: str = Field(default="ru", description="Язык документа")


class FinancialAnalysis(BaseModel):
    """Финансовый анализ"""
    symbol: str = Field(description="Тикер акции или валютная пара")
    current_price: float = Field(description="Текущая цена")
    price_change: float = Field(description="Изменение цены")
    price_change_percent: float = Field(description="Изменение цены в процентах")
    volume: Optional[int] = Field(default=None, description="Объем торгов")
    recommendation: str = Field(description="Рекомендация (buy/sell/hold)")
    risk_level: str = Field(description="Уровень риска (low/medium/high)")


class CodeAnalysis(BaseModel):
    """Анализ кода"""
    language: str = Field(description="Язык программирования")
    lines_of_code: int = Field(ge=0, description="Количество строк кода")
    complexity_score: float = Field(ge=0.0, description="Оценка сложности")
    issues: List[str] = Field(default=[], description="Найденные проблемы")
    suggestions: List[str] = Field(default=[], description="Предложения по улучшению")
    quality_score: float = Field(ge=0.0, le=10.0, description="Оценка качества кода")


class TranslationResult(BaseModel):
    """Результат перевода"""
    original_text: str = Field(description="Исходный текст")
    translated_text: str = Field(description="Переведенный текст")
    source_language: str = Field(description="Исходный язык")
    target_language: str = Field(description="Целевой язык")
    confidence: float = Field(ge=0.0, le=1.0, description="Уверенность в переводе")


class QuestionAnswer(BaseModel):
    """Ответ на вопрос"""
    question: str = Field(description="Заданный вопрос")
    answer: str = Field(description="Ответ на вопрос")
    confidence: float = Field(ge=0.0, le=1.0, description="Уверенность в ответе")
    sources: List[str] = Field(default=[], description="Источники информации")
    category: str = Field(description="Категория вопроса")


class EmailDraft(BaseModel):
    """Черновик электронного письма"""
    subject: str = Field(description="Тема письма")
    body: str = Field(description="Текст письма")
    tone: str = Field(description="Тон письма (formal/informal/friendly)")
    recipient_type: str = Field(description="Тип получателя (colleague/client/friend)")
    estimated_reading_time: int = Field(ge=0, description="Примерное время чтения в секундах")


# === РЕЕСТР МОДЕЛЕЙ ===

RESPONSE_MODELS_REGISTRY: Dict[str, Type[BaseModel]] = {
    "TaskResult": TaskResult,
    "UserAnalysis": UserAnalysis,
    "SearchResult": SearchResult,
    "DocumentSummary": DocumentSummary,
    "FinancialAnalysis": FinancialAnalysis,
    "CodeAnalysis": CodeAnalysis,
    "TranslationResult": TranslationResult,
    "QuestionAnswer": QuestionAnswer,
    "EmailDraft": EmailDraft,
}


def get_response_model(model_name: str) -> Optional[Type[BaseModel]]:
    """
    Получить модель по имени
    
    Args:
        model_name: Имя модели из реестра
        
    Returns:
        Класс Pydantic модели или None если не найдена
    """
    return RESPONSE_MODELS_REGISTRY.get(model_name)


def register_response_model(model_name: str, model_class: Type[BaseModel]):
    """
    Зарегистрировать новую модель
    
    Args:
        model_name: Имя модели
        model_class: Класс Pydantic модели
    """
    RESPONSE_MODELS_REGISTRY[model_name] = model_class


def list_available_models() -> List[str]:
    """
    Список доступных моделей
    
    Returns:
        Список имен доступных моделей
    """
    return list(RESPONSE_MODELS_REGISTRY.keys())


def get_model_schema(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Получить JSON Schema модели
    
    Args:
        model_name: Имя модели
        
    Returns:
        JSON Schema модели или None
    """
    model_class = get_response_model(model_name)
    if model_class:
        return model_class.model_json_schema()
    return None


def get_models_info() -> Dict[str, Dict[str, Any]]:
    """
    Получить информацию о всех моделях
    
    Returns:
        Словарь с информацией о каждой модели
    """
    models_info = {}
    for name, model_class in RESPONSE_MODELS_REGISTRY.items():
        schema = model_class.model_json_schema()
        models_info[name] = {
            "description": schema.get("description", model_class.__doc__ or ""),
            "properties": list(schema.get("properties", {}).keys()),
            "required": schema.get("required", []),
            "example_fields": len(schema.get("properties", {}))
        }
    return models_info 