import psycopg2 as pypg
import json
from algorithm import BatchGraph, risk_judge
import os

conn = pypg.connect(database='postgres', user='postgres', host='39.106.83.49', port='5432')
cursor = conn.cursor()
product = 5


def execute_pg(sql, args=None):
    cursor.execute(sql) if not args else cursor.execute(sql, args)
    try:
        for i in range(cursor.rowcount):
            yield cursor.fetchone()
    except:
        return StopIteration()


def drug_deliver(agent_ph):
    query = f'select deliver_id, distributor_code, amount_factory from deliver{product} where ph_code=%s;'
    records = []
    for row in execute_pg(query, (agent_ph, )):
        deliver_id, distributor_code, amount_factory = row
        records.append([deliver_id, distributor_code, float(amount_factory)])
    return records


def drug_sale(batch):
    query = f'select sale_date, seller_code_ph, seller_province, seller_city, purchaser_code_ph, purchaser_province, ' \
            f'purchaser_city, sale_amount_factory, seller_agent_historical_level,purchaser_agent_historical_level from sale{product} where batch_number=%s order by sale_date;'
    records = []
    for row in execute_pg(query, (batch, )):
        sale_date, seller_code_ph, seller_province, seller_city, purchaser_code_ph, purchaser_province, purchaser_city,\
        sale_amount_factory, seller_agent_historical_level,purchaser_agent_historical_level = row
        records.append([sale_date, seller_code_ph, seller_province, seller_city, purchaser_code_ph, purchaser_province,
                        purchaser_city, float(sale_amount_factory), seller_agent_historical_level,purchaser_agent_historical_level or 'Tier 2'])
    return records


def drug_amount(batch, year, month):
    query = f'select batch_number, purchaser_province, purchaser_city, sale_year, sale_month, amount from sale{product}_amount where batch_number = %s and sale_year = %s and sale_month = %s;'
    records = []
    for row in execute_pg(query, (batch, year, month)):
        batch_number, purchaser_province, purchaser_city, sale_year, sale_month, amount = row
        records.append([batch_number, purchaser_province, purchaser_city, sale_year, sale_month, float(amount)])
    return records


def drug_amount_province(batch, year, month):
    query = f'select purchaser_province, province_amount from sale{product}_amount_province ' \
            f'where batch_number = %s and sale_year = %s and sale_month = %s;'
    records = []
    for row in execute_pg(query, (batch, year, month)):
        purchaser_province, province_amount = row
        records.append([purchaser_province, float(province_amount)])
    return records


def drug_amount_city(batch, year, month, province):
    query = f'select purchaser_city, amount as city_amount from sale{product}_amount ' \
            f'where batch_number = %s and sale_year = %s and sale_month = %s and purchaser_province = %s; '
    records = []
    for row in execute_pg(query, (batch, year, month, province)):
        purchaser_city, city_amount = row
        records.append([purchaser_city, float(city_amount)])
    return records


def save_drug_amount():
    province_query = f'select sale_year, sale_month, purchaser_province, sum(province_amount) as province_amount ' \
                     f'from sale{product}_amount_province ' \
                     f'group by sale_year, sale_month, purchaser_province; '
    city_query = f'select sale_year, sale_month, purchaser_province, purchaser_city, sum(amount) as city_amount ' \
                 f'from sale{product}_amount ' \
                 f'group by sale_year, sale_month, purchaser_province, purchaser_city; '

    with open('province_amount.csv', 'w', encoding='utf-8') as f:
        for row in execute_pg(province_query):
            sale_year, sale_month, purchaser_province, province_amount = row
            f.write(f'{",".join([str(sale_year), str(sale_month), purchaser_province, str(float(province_amount))])}\n')

    with open('city_amount.csv', 'w', encoding='utf-8') as f:
        for row in execute_pg(city_query):
            sale_year, sale_month, purchaser_province, purchaser_city, city_amount = row
            f.write(f'{",".join([str(sale_year), str(sale_month), purchaser_province, purchaser_city, str(float(city_amount))])}\n')



def get_dealers_province(province):
    query = f'select seller_code_ph, seller_province, seller_city ' \
            f'from sale{product}_seller ' \
            f'where seller_province = %s;'
    records = []
    for row in execute_pg(query, (province,)):
        seller_code_ph, seller_province, seller_city = row
        records.append([seller_code_ph, seller_province, seller_city])
    return records

def get_dealers_city(city):
    query = f'select seller_code_ph, seller_province, seller_city ' \
            f'from sale{product}_seller ' \
            f'where seller_city = %s;'
    records = []
    for row in execute_pg(query, (city,)):
        seller_code_ph, seller_province, seller_city = row
        records.append([seller_code_ph, seller_province, seller_city])
    return records


def self_sale_agent():
    query = f'select * from self_sale_agent_{product} ' \
            f'where seller_code_ph = purchaser_code_ph and purchaser_property=\'经销商\';'
    records = []
    for row in execute_pg(query):
        records.append(row)
    return records


def agent_sale_record():
    query = f'select seller_code_ph, purchaser_code_ph, batch_number from sale{product} ' \
            f'where purchaser_property = \'经销商\' ' \
            f'group by seller_code_ph, purchaser_code_ph, batch_number; '

    allsales = {}
    for row in execute_pg(query):
        seller_code_ph, purchaser_code_ph, batch_number = row
        if batch_number not in allsales:
            allsales[batch_number] = {
                'agents': set(),
                'edges': []
            }
        allsales[batch_number]['agents'].update([seller_code_ph, purchaser_code_ph])
        allsales[batch_number]['edges'].append((seller_code_ph, purchaser_code_ph))

    with open('sale-edges-5.json', 'w', encoding='utf-8') as f:
        for batch_number, batch in allsales.items():
            batch['agents'] = list(batch['agents'])
        json.dump(allsales, f, ensure_ascii=False, indent=2)


def risk_detect():
    with open('sale-edges-5.json', 'r', encoding='utf-8') as f:
        sale = json.load(f)
        risk_batch= risk_judge(sale)
        with open('risk_batch.json', 'w', encoding='utf-8') as frb:
            json.dump(risk_batch, frb, ensure_ascii=False, indent=2)


def risk_agent_info():
    with open('risk_batch.json', 'r', encoding='utf-8') as f:
        risk_batch = json.load(f)

    risk_agents = set()
    for agents in risk_batch['self-cycle'].values():
        risk_agents.update(agents)
    for agents in risk_batch['multi-cycle'].values():
        risk_agents.update(agents)

    risk_agents = {
        agent: {
            'ph': agent,
            'area': '',
            'province': '',
            'city': ''
        } for agent in risk_agents
    }
    query = f'select seller_agent_business_area_small, seller_province, seller_city from seller where seller_code_ph = %s;'
    for agent in risk_agents:
        for row in execute_pg(query, (agent, )):
            seller_agent_business_area_small, seller_province, seller_city = row
            risk_agents[agent]['area'] = seller_agent_business_area_small
            risk_agents[agent]['province'] = seller_province
            risk_agents[agent]['city'] = seller_city

    with open('risk_agent_province_city.json', 'w', encoding='utf-8') as f:
        json.dump(risk_agents, f, ensure_ascii=False, indent=2)


def risk_area():
    if os.path.isfile('risk_value.json'):
        with open('risk_value.json', 'r', encoding='utf-8') as f:
            risk_value = json.load(f)
        return risk_value

    with open('risk_agent_province_city.json', 'r', encoding='utf-8') as f:
        risk_agents = json.load(f)
    with open('risk_batch.json', 'r', encoding='utf-8') as f:
        risk_batch = json.load(f)

    aggregated = {}
    for agent_ph, agent in risk_agents.items():
        if agent['area'] not in aggregated:
            aggregated[agent['area']] = {}
        if agent['province'] not in aggregated[agent['area']]:
            aggregated[agent['area']][agent['province']] = {}
        if agent['city'] not in aggregated[agent['area']][agent['province']]:
            aggregated[agent['area']][agent['province']][agent['city']] = {
                'sc-agents': [],
                'mc-agents': []
            }

    for batch_number, batch in risk_batch['self-cycle'].items():
        agent_ph = batch[0]
        agent = risk_agents[agent_ph]
        aggregated[agent['area']][agent['province']][agent['city']]['sc-agents'].append(agent_ph)
    for batch_number, batch in risk_batch['multi-cycle'].items():
        for agent_ph in batch:
            agent = risk_agents[agent_ph]
            aggregated[agent['area']][agent['province']][agent['city']]['mc-agents'].append(agent_ph)
    for area_name, area in aggregated.items():
        arv = 0
        for province_name, province in aggregated[area_name].items():
            prv = 0
            for city_name, city in aggregated[area_name][province_name].items():
                city['risk_value'] = len(city['sc-agents']) + len(city['mc-agents'])
                prv += city['risk_value']
            province['risk_value'] = prv
            arv += prv
        area['risk_value'] = arv

    with open('risk_value.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, ensure_ascii=False, indent=2)

    return aggregated



if __name__ == '__main__':
    product = 5
    # result = drug_deliver('BY100031')
    # result = drug_sale('BJ38668')
    # result = result[:5]
    # print(result)
    # res = get_dealers_city("福州市")
    # print(drug_amount_province('BJ38668', 2018, 6))
    # print(drug_amount_city('BJ38668', 2018, 6, '陕西省'))
    # print(len(self_sale_agent()))
    # agent_sale_record()
    # risk_circle()
    # risk_agent_info()
    # risk_agent_info_area()
    save_drug_amount()
    conn.close()