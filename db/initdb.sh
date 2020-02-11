#!/bin/bash
psql -h "$DB_HOST" --username "$DB_USER" -d "postgres"  <<-EOSQL
CREATE DATABASE account;
SELECT current_database();
EOSQL
psql -v ON_ERROR_STOP=1 -h "$DB_HOST" --username "$DB_USER" -d account  <<-EOSQL
    SELECT current_database();
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE TABLE IF NOT EXISTS public.accounts (
        id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
        fio character varying(225) NOT NULL,
        hold INT NOT NULL,
        current_balans INT NOT NULL,
        status boolean DEFAULT true
    );
    INSERT INTO public.accounts(id, fio, "hold", current_balans, status)
    VALUES ('26c940a1-7228-4ea2-a3bc-e6460b172040', 'Петров Иван Сергеевич',1700, 300, True);

    INSERT INTO public.accounts(id, fio, "hold", current_balans, status)
    VALUES ('7badc8f8-65bc-449a-8cde-855234ac63e1', 'Kazitsky Jason',200, 200, True);

    INSERT INTO public.accounts(id, fio, "hold", current_balans, status)
    VALUES ('5597cc3d-c948-48a0-b711-393edf20d9c0', 'Пархоменко Антон Александрович',10, 300, True);

    INSERT INTO public.accounts(id, fio, "hold", current_balans, status)
    VALUES ('867f0924-a917-4711-939b-90b179a96392', 'Петечкин Петр Измаилович',1000000, 1, False);

EOSQL
