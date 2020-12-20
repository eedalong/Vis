
import os
import datetime
import re

to_datetime = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
to_date = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
to_self = lambda x: x
to_self_cut = lambda x: x.split(' ')[0]
to_bool = lambda x: x in ['1', '是', 'true', 'TRUE', 'True']
def to_bj(x):
    sf = re.search(r'[bB][jJ][0-9]+', x)
    return sf.group(0) if sf else None


class TableRow:
    attr_name_list = []
    converter = []
    type_check_ = None

    def __init__(self, line, no_cvt=False):
        # sf = re.search(r'"([A-Za-z0-9]*)(//[^,"]*)?,([A-Za-z0-9]*)(//[^,"]*)?"', line)
        # if sf:
        #     line = line.replace(sf.group(0), sf.group(1) + sf.group(3))
        ts = line[:-1].split(',')
        # print(len(ts), len(self.attr_name_list), len(self.converter))
        for i, token in enumerate(ts):
            if token.lower() == 'null':
                setattr(self, self.attr_name_list[i], None)
            elif no_cvt:
                setattr(self, self.attr_name_list[i], token)
            else:
                setattr(self, self.attr_name_list[i], self.converter[i](token))

        # for attr_name in self.attr_name_list:
        #     print(f'{attr_name}, {getattr(self, attr_name)}')
        # print('-----------------------------------------------')

    @classmethod
    def type_check(cls):
        if cls.type_check_ is None:
            typemap = {
                int: int,
                float: float,
                to_datetime: datetime.datetime,
                to_date: datetime.datetime,
                to_self: str,
                to_self_cut: str,
                to_bool: bool,
                to_bj: str
            }
            cls.type_check_ = [typemap[j] for j in cls.converter]
        return cls.type_check_

    def to_sqlv(self, table_name):
        nattrs = len(self.attr_name_list)
        template = f'({"%s, " * (nattrs - 1)}{"%s"})'
        attr_names = f'({", ".join(self.attr_name_list)})'
        sql = f'insert into {table_name} {attr_names} values {template};'
        data = tuple([getattr(self, attr) for attr in self.attr_name_list])
        # print(sql)
        return sql, data


class ProductSale(TableRow):
    attr_name_list = [
        'sale_year',
        'sale_month',
        'sale_date',
        'seller_code_PH',
        'seller_agent_historical_level',
        'seller_agent_business_area_small',
        'seller_business_area',
        'seller_sale_area',
        'seller_province',
        'seller_city',
        'seller_city_level',
        'purchaser_code_SFE',
        'purchaser_code_PH',
        'purchaser_business_area',
        'purchaser_sale_area',
        'purchaser_sale_area_2',
        'purchaser_province',
        'purchaser_city',
        'purchaser_city_level',
        'purchaser_admin_code',
        'purchaser_county',
        'purchaser_SFE_terminal_level',
        'purchaser_property',
        'purchaser_category',
        'purchaser_agent_current_level',
        'purchaser_agent_historical_level',
        'purchaser_is_chain_head',
        'purchaser_is_target_terminal',
        'purchaser_is_ticket_business',
        'product_code',
        'product_group',
        'product_line',
        'batch_number',
        'sale_amount_factory',
        'is_cross_business_area',
        'is_cross_province',
        'is_daily_data',
        'method_data_collect',
        'method_real_collect',
        'method_purchaser_manage',
        'is_sub_company',
        'upstream_company_corporation',
        'upstream_company'
    ]

    converter = [
        int,
        int,
        to_datetime,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        int,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        int,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_bool,
        to_bool,
        to_bool,
        int,
        to_self,
        to_self,
        to_bj,
        float,
        to_bool,
        to_bool,
        to_bool,
        to_self,
        to_self,
        to_self,
        to_bool,
        to_self,
        to_self
    ]


class Deliver(TableRow):
    attr_name_list = [
        'deliver_date',
        'distributor_code',
        'ph_code',
        'product_code',
        'amount_factory',
        'com_region',
        'sale_region',
        'province'
    ]
    converter = [
        to_date,
        to_self,
        to_self,
        int,
        float,
        to_self,
        to_self,
        to_self
    ]


class Purchase(TableRow):
    attr_name_list = [
        'purchase_year',
        'purchase_month',
        'purchase_date',
        'seller_code_ph',
        'seller_agent_historical_level',
        'seller_business_area',
        'seller_agent_business_area_small',
        'seller_sale_area',
        'seller_province',
        'seller_city_code',
        'seller_city',
        'seller_city_level',
        'purchaser_code_ph',
        'purchaser_agent_current_level',
        'purchaser_agent_historical_level',
        'purchaser_business_area',
        'purchaser_sale_area',
        'purchaser_province',
        'purchaser_city',
        'purchaser_city_level',
        'purchaser_is_chain_head',
        'product_code',
        'product_group',
        'product_unit',
        'batch_number',
        'sale_amount_factory',
        'is_daily_data',
        'method_data_collect',
        'method_real_collect'
    ]
    converter = [
        int,
        int,
        to_date,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        int,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        to_self,
        int,
        to_bool,
        to_self,
        to_self,
        to_self,
        to_bj,
        float,
        to_bool,
        to_self,
        to_self
    ]



def extract_col_name(fpath):
    with open(fpath, 'r') as f:
        for line in f:
            if ',' in line:
                s = line.split(' ')
                for t in s:
                    if len(t) > 2:
                        print(f"'{t}',")
                        break

