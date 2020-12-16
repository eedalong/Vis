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
            f'purchaser_city, sale_amount_factory from sale{product} where batch_number=%s order by sale_date;'
    print(query)
    records = []
    for row in execute_pg(query, (batch, )):
        sale_date, seller_code_ph, seller_province, seller_city, purchaser_code_ph, purchaser_province, purchaser_city, sale_amount_factory = row
        records.append([sale_date, seller_code_ph, seller_province, seller_city, purchaser_code_ph, purchaser_province,
                        purchaser_city, float(sale_amount_factory)])
    return records


def drug_amount(batch, year, month):
    query = f'select batch_number, purchaser_province, purchaser_city, sale_year, sale_month, amount from sale{product}_amount where batch_number = %s and sale_year = %s and sale_month = %s;'
    records = []
    for row in execute_pg(query, (batch, year, month)):
        batch_number, purchaser_province, purchaser_city, sale_year, sale_month, amount = row
        records.append([batch_number, purchaser_province, purchaser_city, sale_year, sale_month, float(amount)])
    return records

def get_dealers_province(province):
    query = f'select seller_code_ph, seller_province, seller_city from sale{product} where seller_province = %s;'
    records = []
    for row in execute_pg(query, (province,)):
        seller_code_ph, seller_province, seller_city = row
        records.append([seller_code_ph, seller_province, seller_city])
    return records

def get_dealers_city(city):
    query = f'select seller_code_ph, seller_province, seller_city from sale{product} where seller_city = %s;'
    records = []
    for row in execute_pg(query, (city,)):
        seller_code_ph, seller_province, seller_city = row
        records.append([seller_code_ph, seller_province, seller_city])
    return records

if __name__ == '__main__':
    product = 5
    # result = drug_deliver('BY100031')
    #result = drug_sale('BJ38668')
    #result = result[:5]
    res = get_dealers_city("福州市")
    print(res)

    conn.close()