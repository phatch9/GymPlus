"""
SOLID: Dependency Inversion Principle
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class IUserService(ABC):
    """Interface for user operations"""
    
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        pass


class IExerciseService(ABC):
    """Interface for exercise operations"""
    
    @abstractmethod
    def get_all_exercises(self, category: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_exercise_by_id(self, exercise_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_exercise(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_exercise(self, exercise_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def delete_exercise(self, exercise_id: int) -> bool:
        pass


class IWorkoutService(ABC):
    """Interface for workout operations"""
    
    @abstractmethod
    def get_workout_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_workout_by_id(self, workout_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_workout(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_workout(self, workout_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def delete_workout(self, workout_id: int) -> bool:
        pass


class ITodoService(ABC):
    """Interface for todo operations"""
    
    @abstractmethod
    def get_todos(self, user_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def create_todo(self, user_id: int, title: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_todo(self, todo_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def delete_todo(self, todo_id: int) -> bool:
        pass
