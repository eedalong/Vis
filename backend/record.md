后端

## API

获取所有省的销量
```python
result = db_conn.drug_amount_province('BJ38668', 2018, 6)
# result = [
#   ['北京市', 2985067.2], 
#   ['天津市', 1079.2], 
#   ['山东省', 491683.52], 
#   ['新疆维吾尔自治区', 135223.76], 
#   ['河北省', 1036895.36], 
#   ['河南省', 295916.64], 
#   ['甘肃省', 21584.0], 
#   ['辽宁省', 1115892.8], 
#   ['陕西省', 120330.8]
# ]
```

获取某个省所有市的销量
```python
result = db_conn.drug_amount_city('BJ38668', 2018, 6, '陕西省')
# result = [
#   ['宝鸡市', 29138.4], 
#   ['延安市', 15648.4], 
#   ['汉中市', 8094.0], 
#   ['西安市', 67450.0]
# ]

```


### SQL代码备忘

```sql
-- 创建自己卖给自己的经销商的物化视图
create materialized view self_sale_agent_5 as (
  select * from sale5 
  where seller_code_ph = purchaser_code_ph 
  and purchaser_property = '经销商'
);

-- 创建按省聚集的销量统计物化视图
create materialized view sale5_amount_province as (
  select batch_number, purchaser_province, sale_year, sale_month, sum(amount) as province_amount from sale5_amount 
  group by batch_number, purchaser_province, sale_year, sale_month
);

-- 创建按省市聚集的销量统计物化视图
cerate materialized view sale5_amount as (
  select batch_number, purchaser_province, purchaser_city, sale_year, sale_month, sum(sale_amount_factory) as amount 
  from sale5
  where purchaser_property <> '经销商' 
  group by batch_number, purchaser_province, purchaser_city, sale_year, sale_month
);

-- 创建所有不同经销商的物化视图，对ph建立索引
create materialized view sale5_seller as (
  select seller_code_ph, seller_agent_historical_level, seller_province, seller_city 
  from sale5
  group by seller_code_ph, seller_agent_historical_level, seller_province, seller_city
);
create index sale5_seller_ph on sale5_seller(seller_code_ph);

-- 创建所有不同经销商对一批次药品总售出销量的物化视图
create materialized view agent_seller_amount_5 as (
  select seller_code_ph, batch_number, sum(sale_amount_factory) as amount
  from sale5
  group by seller_code_ph, batch_number
);
create index agent_seller_amount_5_seller_ph on agent_seller_amount_5(seller_code_ph);

-- 创建所有不同经销商对一批次药品总买入销量的物化视图
create materialized view agent_purchaser_amount_5 as (
  select purchaser_code_ph, batch_number, sum(sale_amount_factory) as amount
  from sale5 
  where purchaser_property = '经销商'  
  group by purchaser_code_ph, batch_number
);
create index agent_purchaser_amount_5_purchaser_ph on agent_purchaser_amount_5(purchaser_code_ph);

select * from agent_seller_amount_5 join agent_purchaser_amount_5 
  on agent_seller_amount_5.seller_code_ph = agent_purchaser_amount_5.purchaser_code_ph
  and agent_seller_amount_5.batch_number = agent_purchaser_amount_5.batch_number 
  ;

-- 查找所有distinct的交易记录（经销商之间）
select seller_code_ph, purchaser_code_ph, batch_number
  from sale5 
  where purchaser_property = '经销商' and batch_number = 'BJ09768' 
  group by seller_code_ph, purchaser_code_ph, batch_number;
```

### 算法

1. 找出所有的自环结点
2. 找出所有入流量和出流量差异很大的结点
3. 找出对一批药的环