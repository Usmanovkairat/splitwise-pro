"""Run: uvicorn backend.app.main:app --host 127.0.0.1 --port 8000."""
from datetime import date
from threading import RLock
from fastapi import FastAPI, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .domain import DomainError
from .repository import MemoryRepository
from .service import Service
from .schemas import GroupInput, GroupUpdate, MemberInput, ExpenseInput, SettlementInput


def create_app(repository=None, storage='memory'):
    app = FastAPI(title='SplitWise Pro API',version='1.0.0')
    app.state.repository = repository or MemoryRepository()
    app.state.storage = storage
    service = Service(app.state.repository)
    lock = RLock()
    app.add_middleware(CORSMiddleware,allow_origins=['http://127.0.0.1:5173','http://localhost:5173'],allow_methods=['GET','POST','PUT','DELETE'],allow_headers=['Content-Type'])

    @app.exception_handler(DomainError)
    async def domain_error(request, exc): return JSONResponse(status_code=exc.status,content={'detail':exc.detail})
    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        details = '; '.join('.'.join(str(x) for x in e['loc'])+': '+e['msg'] for e in exc.errors())
        return JSONResponse(status_code=422,content={'detail':details})
    @app.get('/api/health')
    def health(): return dict(status='ok',storage=app.state.storage)
    @app.get('/api/groups')
    def groups():
        with lock: return app.state.repository.list('groups')
    @app.post('/api/groups',status_code=201)
    def create_group(data:GroupInput):
        with lock:return service.create_group(data.model_dump())
    @app.get('/api/groups/{group_id}')
    def group(group_id:str):
        with lock:return service.group(group_id)
    @app.put('/api/groups/{group_id}')
    def update_group(group_id:str,data:GroupUpdate):
        with lock:return service.update_group(group_id,data.model_dump())
    @app.delete('/api/groups/{group_id}',status_code=204)
    def delete_group(group_id:str):
        with lock:service.delete_group(group_id)
        return Response(status_code=204)
    @app.get('/api/groups/{group_id}/members')
    def members(group_id:str):
        with lock:return service.list('members',group_id)
    @app.post('/api/groups/{group_id}/members',status_code=201)
    def add_member(group_id:str,data:MemberInput):
        with lock:return service.add_member(group_id,data.model_dump())
    @app.delete('/api/groups/{group_id}/members/{member_id}',status_code=204)
    def remove_member(group_id:str,member_id:str):
        with lock:service.remove_member(group_id,member_id)
        return Response(status_code=204)
    @app.get('/api/groups/{group_id}/expenses')
    def expenses(group_id:str,q:str|None=None,category:str|None=None,date_from:date|None=None,date_to:date|None=None):
        with lock:
            if date_from and date_to and date_from > date_to:raise DomainError('Start date must not follow end date')
            rows=service.list('expenses',group_id)
            return sorted([e for e in rows if (not q or q.casefold() in e['description'].casefold()) and (not category or e['category']==category) and (not date_from or e['date']>=date_from.isoformat()) and (not date_to or e['date']<=date_to.isoformat())],key=lambda e:(e['date'],e['id']),reverse=True)
    @app.post('/api/groups/{group_id}/expenses',status_code=201)
    def add_expense(group_id:str,data:ExpenseInput):
        with lock:return service.expense(group_id,data.model_dump(mode='json'))
    @app.put('/api/groups/{group_id}/expenses/{expense_id}')
    def update_expense(group_id:str,expense_id:str,data:ExpenseInput):
        with lock:return service.expense(group_id,data.model_dump(mode='json'),expense_id)
    @app.delete('/api/groups/{group_id}/expenses/{expense_id}',status_code=204)
    def delete_expense(group_id:str,expense_id:str):
        with lock:service.delete_expense(group_id,expense_id)
        return Response(status_code=204)
    @app.get('/api/groups/{group_id}/balances')
    def balances(group_id:str):
        with lock:return service.balances(group_id)
    @app.get('/api/groups/{group_id}/settlements')
    def settlements(group_id:str):
        with lock:return sorted(service.list('settlements',group_id),key=lambda s:(s['date'],s['id']),reverse=True)
    @app.post('/api/groups/{group_id}/settlements',status_code=201)
    def add_settlement(group_id:str,data:SettlementInput):
        with lock:return service.settlement(group_id,data.model_dump(mode='json'))
    @app.get('/api/groups/{group_id}/analytics')
    def analytics(group_id:str):
        with lock:return service.analytics(group_id)
    return app

app = create_app()
