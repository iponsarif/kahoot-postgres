--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7
-- Dumped by pg_dump version 10.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
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


--
-- Name: fnInsertQuizBy_username(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public."fnInsertQuizBy_username"(uname character varying, _title character varying, _category character varying) RETURNS void
    LANGUAGE sql
    AS $$INSERT INTO
quizzess (id, creator_id, title, category, created_at, modified_at, deleted_at)
VALUES (DEFAULT, (select id from users where username = uname), _title, _category, CURRENT_TIMESTAMP, NULL, NULL);$$;


ALTER FUNCTION public."fnInsertQuizBy_username"(uname character varying, _title character varying, _category character varying) OWNER TO postgres;

--
-- Name: FUNCTION "fnInsertQuizBy_username"(uname character varying, _title character varying, _category character varying); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public."fnInsertQuizBy_username"(uname character varying, _title character varying, _category character varying) IS 'insert into quiz by username ';


--
-- Name: fnInsertUser(character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public."fnInsertUser"(uname character varying, pwd character varying, fname character varying, e character varying) RETURNS void
    LANGUAGE sql
    AS $$INSERT INTO
users (id, username, password, fullname, email, created_at, modified_at, deleted_at)
VALUES (DEFAULT, uname, pwd, fname, e, CURRENT_TIMESTAMP, NULL, NULL)$$;


ALTER FUNCTION public."fnInsertUser"(uname character varying, pwd character varying, fname character varying, e character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.games (
    game_pin integer NOT NULL,
    quiz_id integer NOT NULL
);


ALTER TABLE public.games OWNER TO postgres;

--
-- Name: leaderboards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leaderboards (
    game_pin integer NOT NULL,
    participant character varying(20) NOT NULL,
    score integer
);


ALTER TABLE public.leaderboards OWNER TO postgres;

--
-- Name: options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.options (
    id integer NOT NULL,
    question_id integer NOT NULL,
    a character varying(100),
    b character varying(100),
    c character varying(100),
    d character varying(100)
);


ALTER TABLE public.options OWNER TO postgres;

--
-- Name: options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.options_id_seq OWNER TO postgres;

--
-- Name: options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.options_id_seq OWNED BY public.options.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    quiz_id integer NOT NULL,
    question character varying(300) NOT NULL,
    number integer NOT NULL,
    answer character varying(50) NOT NULL,
    created_at timestamp(6) with time zone,
    modified_at timestamp(6) with time zone,
    deleted_at timestamp(6) with time zone
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.questions_id_seq OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: quizzess; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quizzess (
    id integer NOT NULL,
    creator_id integer NOT NULL,
    title character varying(300) NOT NULL,
    category character varying(100) NOT NULL,
    created_at timestamp(6) with time zone,
    modified_at timestamp(6) with time zone,
    deleted_at timestamp(6) with time zone
);


ALTER TABLE public.quizzess OWNER TO postgres;

--
-- Name: quizzess_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quizzess_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quizzess_id_seq OWNER TO postgres;

--
-- Name: quizzess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quizzess_id_seq OWNED BY public.quizzess.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    fullname character varying(200) NOT NULL,
    email character varying(100) NOT NULL,
    created_at timestamp(6) with time zone,
    modified_at timestamp(6) with time zone,
    deleted_at timestamp(6) with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vwAllQuizzessWithUsername; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."vwAllQuizzessWithUsername" AS
 SELECT users.username,
    quizzess.title,
    quizzess.category
   FROM (public.users
     JOIN public.quizzess ON ((users.id = quizzess.creator_id)));


ALTER TABLE public."vwAllQuizzessWithUsername" OWNER TO postgres;

--
-- Name: VIEW "vwAllQuizzessWithUsername"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW public."vwAllQuizzessWithUsername" IS 'view username, title, category from quizzess join users';


--
-- Name: vwAllUsers; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public."vwAllUsers" AS
 SELECT users.id,
    users.username,
    users.password,
    users.fullname,
    users.email,
    users.created_at,
    users.modified_at,
    users.deleted_at
   FROM public.users;


ALTER TABLE public."vwAllUsers" OWNER TO postgres;

--
-- Name: options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options ALTER COLUMN id SET DEFAULT nextval('public.options_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Name: quizzess id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzess ALTER COLUMN id SET DEFAULT nextval('public.quizzess_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.games (game_pin, quiz_id) FROM stdin;
300112	1
821326	1
694405	1
257458	2
945016	2
138330	3
496463	3
940369	4
579653	4
425096	4
915391	5
\.


--
-- Data for Name: leaderboards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leaderboards (game_pin, participant, score) FROM stdin;
300112	danur	0
300112	ahadfashya	0
300112	deri	0
300112	imam	0
915391	imam	0
915391	adit	0
300112	kesatu	200
300112	kedua	400
300112	ketiga	100
821326	akmal	0
821326	imam	0
821326	ican	0
821326	ipon	0
821326	deri	300
821326	adit	400
821326	ahmad	400
821326	firman	600
\.


--
-- Data for Name: options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.options (id, question_id, a, b, c, d) FROM stdin;
8	1	Anjing	Kucing	Tikus	Burung
9	2	Tikus	Kucing	Harimau	Burung
10	3	Kucing	Tikus	Harimau	Serigala
13	10	Kucing	Harimau	Tikus	Serigala
15	12	bonsai	kaktus	alga	lumut
16	13	bonsai	kaktus	alga	lumut
17	14	bonsai	kaktus	alga	lumut
18	15	bonsai	kaktus	alga	lumut
19	16	bonsai	kaktus	alga	lumut
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, quiz_id, question, number, answer, created_at, modified_at, deleted_at) FROM stdin;
1	1	Apakah nama hewan ini?	1	a	\N	\N	\N
3	1	Apakah nama hewan ini?	2	b	\N	\N	\N
2	1	Apakah nama hewan ini?	3	c	\N	\N	\N
10	1	Apakah nama hewan ini?	4	D	\N	\N	\N
12	2	Apakah nama tumbuhan ini?	1	a	\N	\N	\N
13	2	Apakah nama tumbuhan ini?	2	b	\N	\N	\N
14	2	Apakah nama tumbuhan ini?	3	b	\N	\N	\N
15	2	Apakah nama tumbuhan ini?	4	d	\N	\N	\N
16	2	Apakah nama tumbuhan ini?	5	d	\N	\N	\N
\.


--
-- Data for Name: quizzess; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quizzess (id, creator_id, title, category, created_at, modified_at, deleted_at) FROM stdin;
1	1	Nama hewan	Animal	2019-03-08 00:04:39.688081+07	\N	\N
2	1	Kenalkah anda dengan saya	Fun	2019-03-08 00:49:02.313374+07	\N	\N
3	2	Berapakah penjumlahan ini?	Math	2019-03-08 09:22:08.830779+07	\N	\N
4	2	Berapakah perkalian ini?	Math	2019-03-08 09:22:47.542993+07	\N	\N
5	2	Berapa ... bumi ini?	Math	2019-03-08 09:23:20.426874+07	\N	\N
6	2	Kenapa maju itu ke depan?	Fun	2019-03-08 09:23:53.413761+07	\N	\N
7	3	Multi digit numbers	Math	2019-03-08 09:25:17.158551+07	\N	\N
8	3	Finding multiple of 3	Math	2019-03-08 09:25:41.381936+07	\N	\N
9	3	Analyzing Data	Science	2019-03-08 09:27:23.075753+07	\N	\N
10	3	Analog vs Digital	Science	2019-03-08 09:27:36.299509+07	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, fullname, email, created_at, modified_at, deleted_at) FROM stdin;
1	iponsarif	1dong	Ipon Sarif Hidayat	iponsarif@gmail.com	2019-03-07 23:48:29.873611+07	\N	\N
2	fasyahmad	fasyahmad	Ahmad Fasya	fasyahmad@gmail.com	2019-03-07 23:57:29.078451+07	\N	\N
3	neofa	neofa	Muhammad Ihsan	ican@gmail.com	2019-03-07 23:57:29.078451+07	\N	\N
4	runa	runa	Danur Annisa	runa@gmail.com	2019-03-07 23:57:29.078451+07	\N	\N
5	adityaabu	adityaabu	Aditya Abu	adityaabu@gmail.com	2019-03-07 23:57:29.078451+07	\N	\N
6	deriandrian	deriandrian	Deri Andrian	deriandrian@hotmail.com	2019-03-07 23:57:29.078451+07	\N	\N
7	imhwari	imhwari	Imam Akbar	imhwari@hotmail.com	2019-03-08 00:30:39.503297+07	\N	\N
10	gajadites1111	tessssssssssss	tes fullname	tes@gmail.com	2019-03-11 09:34:03.535175+07	\N	\N
13	tes3	tespassword	tes fullname	tes3@gmail.com	2019-03-11 21:59:41.405246+07	\N	\N
15	tes4	tespassword	tes fullname	tes4@gmail.com4	2019-03-13 09:30:33.424798+07	\N	\N
12	tes1	tespassword	tes fullname	tes2@gmail.com	2019-03-11 10:05:21.220572+07	\N	\N
\.


--
-- Name: options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.options_id_seq', 19, true);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 16, true);


--
-- Name: quizzess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quizzess_id_seq', 13, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 18, true);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_pin);


--
-- Name: options options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: quizzess quizzess_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzess
    ADD CONSTRAINT quizzess_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: games games_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzess(id);


--
-- Name: leaderboards leaderboards_game_pin_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leaderboards
    ADD CONSTRAINT leaderboards_game_pin_fkey FOREIGN KEY (game_pin) REFERENCES public.games(game_pin);


--
-- Name: options options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: questions questions_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzess(id);


--
-- Name: quizzess quizzess_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzess
    ADD CONSTRAINT quizzess_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

