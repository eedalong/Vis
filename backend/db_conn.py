import psycopg2 as pypg

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


if __name__ == '__main__':
    product = 5
    # result = drug_deliver('BY100031')
    # result = drug_sale('BJ38668')
    # result = result[:5]
    # print(result)
    res = get_dealers_city("福州市")
    print(res)
    # print(drug_amount_province('BJ38668', 2018, 6))
    # print(drug_amount_city('BJ38668', 2018, 6, '陕西省'))
    print(len(self_sale_agent()))
    conn.close()