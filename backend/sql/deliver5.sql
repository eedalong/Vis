drop table if exists deliver5;
create table deliver5 (
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
