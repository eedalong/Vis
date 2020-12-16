drop table if exists deliver6;
create table deliver6 (
    deliver_id serial primary key,
    deliver_date timestamp,
    distributor_code varchar(8),
    ph_code varchar(16),
    product_code integer,
    amount_factory decimal(12, 2),
    com_region varchar(16),
    sale_region varchar(16),
    province varchar(16)
);
