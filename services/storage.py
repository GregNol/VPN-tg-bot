import logging
from typing import cast
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from core import domain
from services.db import models

logger = logging.getLogger(__name__)


class TaskNotFoundException(Exception):
    """
    Задачи с таким id не существует
    """
    def __init__(self, task_id: int):
        super().__init__(f"Task not found: {task_id}")


class TaskManager:
    def __init__(self, conn: AsyncSession):
        self._db = conn
        
    async def get_tasks(self, **filters):
        """
        filters: параметры фильтрации задач
        return: list[TaskRecord]

        Если не переданы параметры фильтрации - вернёт все задачи.
        Если переданы параметры фильтрации, отфильтрует все задачи по ним и вернет подходящие.
        Если фильтры переданы, но нет подходящих задач, или хранилище пустое
        - вернётся пустой список.
        """
        stmt = select(models.Task)

        if filters:
            for key, value in filters.items():
                if not hasattr(models.Task, key):
                    raise ValueError(f'Class `models.Task` doesn\'t have argument {key}')
            stmt = stmt.filter_by(**filters)

        result = await self._db.execute(stmt)
        models_list = result.scalars().all()
        return [m.to_domain() for m in models_list]

    async def del_task(self, task_id: int) -> domain.TaskRecord:
        """
        task_id: id задачи, которую необходимо удалить
        return: удаленная задача в формате domain.TaskRecord
        
        Если задачи с таким id не существует, возвращает TaskNotFoundException.
        """
        stmt = select(models.Task).filter_by(id=task_id)
        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise TaskNotFoundException(task_id)

        # remove and commit
        await self._db.delete(model)
        await self._db.commit()
        logger.info(f'Удалена задачи с id {task_id}')
        return model.to_domain()
    
    
    async def task(self, task_id: int):
        """
        task_id: id задачи, которую необходимо получить
        return: TaskRecord с указанным task_id
        
        Если задачи с таким id не существует, возвращает TaskNotFoundException.
        """
        stmt = select(models.Task).filter_by(id=task_id)
        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise TaskNotFoundException(task_id)
        return model.to_domain()
    
    async def update_task(self, task_id: int, **kwargs) -> domain.TaskRecord:
        """
        task_id: id задачи, которую необходимо обновить
        kwargs: поля и их новые значения
        return: TaskRecord с измененными параметрами
        
        Если задачи с таким id не существует, возвращает TaskNotFoundException.
        """
        stmt = select(models.Task).filter_by(id=task_id)
        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise TaskNotFoundException(task_id)
        for key, value in kwargs.items():
            if not hasattr(models.Task, key):
                raise ValueError(f'Class `models.Task` doesn\'t have argument {key}')
        stmt = \
            update(models.Task).      \
            filter_by(id=task_id).    \
            values(**kwargs)
        await self._db.execute(stmt)
        await self._db.commit()
        logger.info(f'Обновлена задача с id {task_id}')
        return model.to_domain()

    async def add_task(self, task: domain.Task) -> domain.TaskRecord:
        """
        task: domain.Task - задача для создания (без id)
        return: domain.TaskRecord - созданная задача с id и полями времени
        
        Создаёт новую задачу на основе domain.Task и возвращает domain.TaskRecord.
        """
        if not isinstance(task, domain.Task):
            raise ValueError("task must be an instance of domain.Task")

        model = models.Task.from_domain(task)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        logger.info(f'Создана задача с id {cast(int, model.id)}')
        return model.to_domain()