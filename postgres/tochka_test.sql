--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12
-- Dumped by pg_dump version 10.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tochka_test; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE tochka_test WITH TEMPLATE = template0 ENCODING = 'UTF8';

-- CREATE DATABASE tochka_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.UTF-8' LC_CTYPE = 'ru_RU.UTF-8';

ALTER DATABASE tochka_test OWNER TO postgres;

\connect tochka_test

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying(128),
    account numeric(12,2),
    hold numeric(12,2),
    status boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, account, hold, status) FROM stdin;
26c940a1-7228-4ea2-a3bc-e6460b172040	Петров Иван Сергеевич	1700.00	300.00	t
7badc8f8-65bc-449a-8cde-855234ac63e1	Kazitsky Jason	200.00	200.00	t
867f0924-a917-4711-939b-90b179a96392	Петечкин Петр Измаилович	1000000.00	1.00	f
5597cc3d-c948-48a0-b711-393edf20d9c0	Пархоменко Антон Александрович	300.00	10.00	t
\.


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_name ON public.users USING btree (name);


--
-- PostgreSQL database dump complete
--

