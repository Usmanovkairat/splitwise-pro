import random
import pytest
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.domain import allocate

@pytest.fixture
def client():
    return TestClient(create_app())

def workspace(client):
    g=client.post('/api/groups',json={'name':'Friends','currency':'KZT','description':'Trip'}).json()
    members=[client.post(f"/api/groups/{g['id']}/members",json={'name':n}).json() for n in ('Alice','Bob','Cara')]
    return f"/api/groups/{g['id']}",[m['id'] for m in members]

def expense(ids,**changes):
    return {'description':'Dinner','amount_minor':1001,'payer_id':ids[0],'category':'Food','date':'2026-10-20','split_type':'equal','split_values':{i:1 for i in ids},**changes}

def test_crud_and_isolation(client):
    p,ids=workspace(client)
    assert len(client.get('/api/groups').json())==1
    assert client.put(p,json={'name':'Renamed','description':'New'}).json()['name']=='Renamed'
    e=client.post(p+'/expenses',json=expense(ids)).json()
    assert sum(s['amount_minor'] for s in e['shares'])==1001
    assert client.delete(p+'/members/'+ids[0]).status_code==409
    p2,other=workspace(client)
    assert client.put(p2+'/expenses/'+e['id'],json=expense(other)).status_code==404
    assert client.delete(p2+'/members/'+ids[0]).status_code==404
    assert client.put(p+'/expenses/'+e['id'],json=expense(ids,amount_minor=900)).json()['amount_minor']==900
    assert client.delete(p+'/expenses/'+e['id']).status_code==204
    assert client.delete(p+'/members/'+ids[0]).status_code==204
    assert client.delete(p).status_code==204
    assert client.get(p+'/expenses').status_code==404
    assert len(client.get(p2+'/members').json())==3

@pytest.mark.parametrize('method,values,expected',[('equal',{'b':1,'a':1,'c':1},[334,334,333]),('exact',{'a':500,'b':501},[500,501]),('percentage',{'a':3333,'b':6667},[334,667]),('percentage',{'b':5000,'a':5000},[501,500]),('percentage',{'a':0,'b':10000},[0,1001])])
def test_rounding(method,values,expected):
    assert [s['amount_minor'] for s in allocate(1001,method,values)]==expected

def test_mathematical_invariants():
    rng=random.Random(42)
    for _ in range(250):
        n=rng.randrange(1,10); amount=rng.randrange(1,10000000)
        ids=[f'm{i}' for i in range(n)]
        points=sorted([0,10000]+[rng.randrange(10001) for _ in range(n-1)])
        weights={k:points[i+1]-points[i] for i,k in enumerate(ids)}
        for method,values in [('equal',{k:1 for k in ids}),('percentage',weights)]:
            shares=allocate(amount,method,values)
            assert sum(s['amount_minor'] for s in shares)==amount
            assert all(s['amount_minor']>=0 for s in shares)
            assert shares==allocate(amount,method,dict(reversed(list(values.items()))))

@pytest.mark.parametrize('change',[{'amount_minor':0},{'amount_minor':1.5},{'amount_minor':True},{'amount_minor':10**12+1},{'description':'  '},{'date':'bad'},{'date':0},{'date':'20261020'},{'date':'2026-02-30'},{'payer_id':'foreign'},{'split_values':{}},{'split_values':{'foreign':1}},{'split_type':'exact','split_values':{'bad':1}}])
def test_invalid_expenses_are_atomic(client,change):
    p,ids=workspace(client)
    assert client.post(p+'/expenses',json=expense(ids,**change)).status_code==422
    assert client.get(p+'/expenses').json()==[]

@pytest.mark.parametrize('method,values',[('exact',[1,2,3]),('percentage',[100,200,300]),('percentage',[5000,5000.5,0]),('equal',[-1,1,1])])
def test_invalid_split_totals(client,method,values):
    p,ids=workspace(client)
    assert client.post(p+'/expenses',json=expense(ids,split_type=method,split_values=dict(zip(ids,values)))).status_code==422

def test_partial_settlement_and_analytics(client):
    p,ids=workspace(client)
    client.post(p+'/expenses',json=expense(ids,amount_minor=900))
    b=client.get(p+'/balances').json()
    assert sum(m['net_minor'] for m in b['members'])==0
    assert sum(s['amount_minor'] for s in b['suggestions'])==600
    data={'from_member_id':ids[1],'to_member_id':ids[0],'amount_minor':100,'date':'2026-10-20','note':'Partial'}
    assert client.post(p+'/settlements',json=data).status_code==201
    b=client.get(p+'/balances').json(); rows={m['member_id']:m for m in b['members']}
    assert rows[ids[1]]['net_minor']==-200
    assert rows[ids[0]]['net_minor']==500
    assert sum(m['net_minor'] for m in b['members'])==0
    a=client.get(p+'/analytics').json()
    assert a['total_minor']==900 and a['outstanding_minor']==500
    assert a['by_category']==[{'category':'Food','amount_minor':900}]
    assert a['over_time']==[{'date':'2026-10-20','amount_minor':900}]
    assert sum(m['amount_minor'] for m in a['contributions'])==900
    assert len(client.get(p+'/settlements').json())==1
    assert client.post(p+'/settlements',json={**data,'amount_minor':201}).status_code==422
    assert client.post(p+'/settlements',json={**data,'from_member_id':ids[0],'to_member_id':ids[1]}).status_code==422
    assert client.post(p+'/settlements',json={**data,'to_member_id':ids[1]}).status_code==422
    assert client.post(p+'/settlements',json={**data,'from_member_id':'foreign'}).status_code==422


def test_filters_and_validation(client):
    p,ids=workspace(client)
    client.post(p+'/expenses',json=expense(ids))
    assert len(client.get(p+'/expenses?q=DIN&category=Food&date_from=2026-10-20&date_to=2026-10-20').json())==1
    assert client.get(p+'/expenses?q=nope').json()==[]
    assert client.get(p+'/expenses?date_from=2026-10-21&date_to=2026-10-20').status_code==422
    for data in [{'name':' ','currency':'KZT','description':''},{'name':'test','currency':'JPY','description':''}]:
        assert client.post('/api/groups',json=data).status_code==422
    assert client.get('/api/health').json()=={'status':'ok','storage':'memory'}
    assert client.get('/api/groups/missing').status_code==404
    assert isinstance(client.post('/api/groups',json={}).json()['detail'],str)
