import psycopg2 as pypg
import os
import datetime
import re
import sys

from models import TableRow, ProductSale, Deliver, Purchase
import db_conn


def test_pg_conn():
    conn = pypg.connect(database='postgres', user='postgres', host='39.106.83.49', port='5432')
    cursor = conn.cursor()
    cursor.execute('select * from information_schema.columns where table_name=\'test1\';')
    rows = cursor.fetchone()
    print(rows)
    conn.close()


def execute(sql, args=None):
    results = []
    conn = pypg.connect(database='postgres', user='postgres', host='39.106.83.49', port='5432')
    cursor = conn.cursor()
    cursor.execute(sql) if not args else cursor.execute(sql, args)
    conn.commit()
    try:
        for row in cursor.fetchall():
            print(row)
            results.append(row)
    except:
        pass
    conn.close()
    return results


def real_load(fpath, model: TableRow.__class__, table_name, host, start):
    conn = pypg.connect(database='postgres', user='postgres', host=host, port='5432')
    cursor = conn.cursor()

    with open(fpath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < start:
                continue
            sale = model(line, no_cvt=i == 0)
            if i >= 1:
                try:
                    sql, args = sale.to_sqlv(table_name)
                    cursor.execute(sql, args)
                except Exception as e:
                    print(e)
                    print(f'Line {i} error')
                    break
            if i % 1000 == 0:
                print(i)
                conn.commit()
        conn.commit()
    conn.close()


def try_load(fpath, model: TableRow.__class__):
    print(len(model.attr_name_list), len(model.converter))
    with open(fpath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            item = model(line, no_cvt=i == 0)
            if i > 0:
                try:
                    for attr_name, attr_type in zip(item.attr_name_list, item.type_check()):
                        assert getattr(item, attr_name) is None or isinstance(getattr(item, attr_name), attr_type)
                except Exception as e:
                    print(i, attr_name, attr_type, getattr(item, attr_name))
                    raise e


def seek(i, tj):
    product5_sale_path = 'bayer_raw__data\\' + purchase5
    sets = set()
    with open(product5_sale_path, 'r', encoding='utf-8') as f:
        for j, line in enumerate(f):
            if tj == j:
                print(line)
                break
            if j >= tj:
                try:
                    sf = re.search(r'"([A-Za-z0-9]*)(//[^,"]*)?,([A-Za-z0-9]*)(//[^,"]*)?"', line)
                    if sf:
                        line = line.replace(sf.group(0), sf.group(1) + sf.group(3))
                    float(line.split(',')[33])
                except:
                    print(j, line)
    print(j)
    c = 0
    for k in sets:
        print(k)
        c += 1
        if c > 100:
            break


def execute_sql(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        sql = f.read()

    print(sql)
    execute(sql)


def fix_batch_number(fpath):
    qc = r'"(.*),(.*)"'

    template = r'[Bb][A-Za-z0-9]+'
    errcount = 0
    with open('out5.txt', 'w', encoding='utf-8') as fo:
        with open(fpath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                if i % 10000 == 0:
                    print(i)
                qcm = re.search(qc, line[:-1])
                if qcm:
                    re.sub(qcm.group(0), f'"{qcm.group(1)} {qcm.group(2)}"', line)
                batch_number_cand = line.split(',')[32]

                if len(batch_number_cand) == 7:
                    fo.write(f'{batch_number_cand}\n')
                    continue
                elif len(batch_number_cand) == 0:
                    fo.write(f'\n')
                    continue

                search = re.search(template, batch_number_cand)
                if search:
                    fo.write(f'{search.group(0)}\n')
                else:
                    if len(batch_number_cand) > 4:
                        errcount += 1
                    fo.write('\n')
                    # print('Error ', i, batch_number_cand)
    print(errcount)


def fix_batch_number_load(fpath, start):
    conn = pypg.connect(database='postgres', user='postgres', host=host, port='5432')
    cursor = conn.cursor()

    with open(fpath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < start:
                continue
            template = 'update sale5 set batch_number = %s where product_sale_id = %s;'
            new_bn = line[:-1]
            if new_bn == '':
                new_bn = None
            cursor.execute(template, (new_bn, i + 1))

            if (i + 1) % 10000 == 0:
                print(i + 1, flush=True)
                # break
                conn.commit()
        conn.commit()
    conn.close()


def sample(inpath, outpath):
    with open(outpath, 'w', encoding='utf-8') as fo:
        with open(inpath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                fo.write(line)
                if i > 100:
                    break


def get_all_agent_ph():
    views = {
        'seller': 'create materialized view seller as (select distinct seller_code_PH, '
                  'seller_agent_historical_level, '
                  'seller_business_area,'
                  'seller_agent_business_area_small,'
                  'seller_province,'
                  'seller_city '
                  'from sale5) union  (select distinct seller_code_PH, '
                  'seller_agent_historical_level, '
                  'seller_business_area,'
                  'seller_agent_business_area_small,'
                  'seller_province,'
                  'seller_city '
                  'from sale6)',
        'purchaser': 'create materialized view purchaser as (select distinct purchaser_code_PH, '
                     'purchaser_business_area,'
                     'purchaser_province,'
                     'purchaser_city,'
                     'purchaser_county,'
                     'purchaser_property,'
                     'purchaser_agent_current_level '
                     'from sale5) union (select distinct purchaser_code_PH, '
                     'purchaser_business_area,'
                     'purchaser_province,'
                     'purchaser_city,'
                     'purchaser_county,'
                     'purchaser_property,'
                     'purchaser_agent_current_level '
                     'from sale6)'
    }
    r = execute(views['purchaser'])
    print(r)
    # agent_ph_in_sale5 = execute('select distinct seller_code_PH ')


def max_level():
    conn = pypg.connect(database='postgres', user='postgres', host=host, port='5432')
    cursor = conn.cursor()
    cursor.execute('select * from seller;')
    wls = {
        'Tier 1': 1,
        'Key Tier 2': 2,
        'Tier 2': 3,
        'Tier 3': 4,
        'Other': 5,
        'other': 5,
        None: 6
    }
    levels = {

    }
    rev_wls = {
        1: 'Tier 1',
        2: 'Key Tier 2',
        3: 'Tier 2',
        4: 'Tier 3',
        5: 'Other',
        6: None
    }
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        lvl = row[1]
        ph = row[0]
        if lvl not in levels:
            levels[ph] = wls[lvl]
        else:
            levels[ph] = min(levels[ph], wls[lvl])
    print(len(levels), i)
    for ph, lvl in levels.items():
        cursor.execute('update sale6 set seller_agent_historical_level = %s where seller_code_ph = %s;',
                       (rev_wls[lvl], ph))
    conn.commit()
    # cursor.execute('create materialized view seller_d (select distinct * from seller);')
    # conn.commit()


if __name__ == "__main__":
    print(sys.argv)
    host = '39.106.83.49' if sys.argv[1] == 'remote' else '127.0.0.1'
    start = int(sys.argv[2])
    purchase5 = '2015-2019产品5采购数据.csv'
    purchase6 = '2015-2019产品6采购数据.csv'
    sale5 = 'product5_sale.csv'
    sale6 = '2015-2019产品6销售数据.csv'
    deliver5 = '2017-2019产品5SAP发货数据.csv'
    deliver6 = '2017-2019产品6SAP发货数据.csv'

    # max_level()
    # db_conn.construct_seller_node()
    # db_conn.test_neo4j_connection()
    # fix_batch_number_load('out5.txt', 0)
    # fix_batch_number(os.path.join('bayer_raw__data', sale5))
    # get_all_agent_ph()
    # execute_sql(os.path.join('sql', 'sale6.sql'))
    # real_load(os.path.join('bayer_raw__data', sale6), ProductSale, 'sale6', host, start)
    # try_load(os.path.join('bayer_raw__data', sale6), Sale6)
    # seek(0, 48594)
    # load_data()
    # test()
    # seek(4)
    # test_pg_conn()
    # load_data()
    # for path in os.listdir('bayer_raw__data'):
    #     sample(os.path.join('bayer_raw__data', path), os.path.join('sampled', path))
