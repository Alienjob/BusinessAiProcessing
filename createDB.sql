create schema business_ai;

create table business_ai.ai_plans
(
    prompt_id uuid,
    dtype varchar(31) not null,
    fname varchar(512) not null,
    cron_expression varchar(64),
    primary key (fname)
);

create table business_ai.application
(
    fgroup      varchar(512),
    fname       varchar(512) not null,
    description text,
    primary key (fname)
);

create table business_ai.ass_analog
(
    analogies_id  uuid not null,
    assortment_id uuid not null
);

create table business_ai.ass_attach
(
    assortment_id uuid not null,
    mime          varchar(64),
    store_id      varchar(64),
    filename      varchar(2000)
);

create table business_ai.ass_image
(
    assortment_id uuid not null,
    images        varchar(255)
);

create table business_ai.ass_props
(
    assortment_id            uuid        not null,
    properties_goods_prop_id varchar(64) not null
);

create table business_ai.assortment
(
    fmode        smallint check (fmode between 0 and 2),
    barcode      varchar(13),
    id           uuid not null,
    issuer_id    uuid,
    manufacturer uuid,
    article      varchar(64),
    measure      varchar(64),
    ok_code      varchar(64),
    fname        varchar(512),
    trademark    varchar(512),
    description  text,
    primary key (id)
);

create table business_ai.auth_info
(
    auth_type   smallint     not null check (auth_type between 0 and 2),
    user_id     uuid         not null,
    flogin      varchar(512),
    condition   varchar(2000),
    application varchar(255) not null,
    primary key (auth_type, user_id, application)
);

create table business_ai.auth_locate
(
    latitude  varchar(12),
    longitude varchar(12),
    ip        varchar(15),
    id        uuid not null,
    user_id   uuid,
    fname     varchar(512),
    primary key (id)
);

create table business_ai.bank
(
    address_id   uuid,
    bik          varchar(64)  not null,
    correspond   varchar(64),
    kladr        varchar(64),
    swift        varchar(64),
    fname        varchar(512) not null,
    full_address varchar(2000),
    primary key (bik, fname)
);

create table business_ai.bank_contact
(
    bank_info_bik   varchar(64)  not null,
    cont_kind       varchar(64),
    bank_info_fname varchar(512) not null,
    contact         varchar(512),
    cont_comment    varchar(2000)
);

create table business_ai.bank_rekv
(
    seller_id uuid         not null,
    account   varchar(64)  not null,
    bik       varchar(64)  not null,
    inn       varchar(64),
    kpp       varchar(64),
    bank_name varchar(512) not null,
    rname     varchar(512),
    primary key (seller_id, account, bank_name, bik)
);

create table business_ai.collection
(
    fname       varchar(512) not null,
    description text,
    primary key (fname)
);

create table business_ai.communities
(
    user_id   uuid         not null,
    community varchar(512) not null
);

create table business_ai.community
(
    status smallint check (status between 0 and 4),
    fapp   varchar(512),
    fname  varchar(512) not null,
    primary key (fname)
);

create table business_ai.cust_requests
(
    frate           float4,
    fstate          smallint check (fstate between 0 and 4),
    created_at      timestamp(6) not null,
    organization_id uuid         not null,
    prompt_id       uuid,
    platform_id     varchar(64),
    ai_provider     varchar(512),
    client          varchar(512) not null,
    platform        varchar(512),
    answer_text     text,
    request_text    text,
    satisfaction    real,
    primary key (created_at, organization_id, client),
    unique (platform_id, platform)
);

create table business_ai.image_description
(
    assortment_id uuid         not null,
    prompt_id     uuid,
    image_name    varchar(255) not null,
    fcontent      text,
    primary key (assortment_id, image_name)
);

create table business_ai.org_ai_plans
(
    org_id    uuid         not null,
    plan_name varchar(512) not null
);

create table business_ai.org_attachment
(
    organization_id uuid not null,
    mime            varchar(64),
    store_id        varchar(64),
    filename        varchar(2000)
);

create table business_ai.org_contact
(
    organization_id uuid not null,
    cont_kind       varchar(64),
    contact         varchar(512),
    cont_comment    varchar(2000)
);

create table business_ai.org_director
(
    organization_id  uuid not null,
    director_id_list varchar(255)
);

create table business_ai.org_group
(
    group_id uuid not null,
    org_id   uuid not null
);

create table business_ai.org_license
(
    license_end    date,
    license_start  date,
    issuer         uuid        not null,
    licentiate     uuid        not null,
    license_number varchar(64) not null,
    license_addr   varchar(2000),
    license_descr  varchar(2000),
    primary key (issuer, licentiate, license_number)
);

create table business_ai.org_link_prop
(
    fkind      smallint not null,
    value_kind smallint check (value_kind between 0 and 8),
    vbool      boolean,
    vdate      date,
    vfloat     numeric(38, 2),
    vlong      bigint,
    vtimestamp timestamp(6),
    dest_id    uuid     not null,
    source_id  uuid     not null,
    vguid      uuid,
    prop_name  varchar(512),
    vstring    varchar(2000),
    bstring    text
);

create table business_ai.org_prop
(
    value_kind smallint check (value_kind between 0 and 8),
    vbool      boolean,
    vdate      date,
    vfloat     numeric(38, 2),
    vlong      bigint,
    vtimestamp timestamp(6),
    org_id     uuid not null,
    vguid      uuid,
    prop_name  varchar(512),
    vstring    varchar(2000),
    bstring    text
);

create table business_ai.organization
(
    capital         float(53),
    defunct         boolean,
    fend            date,
    fkind           smallint check (fkind between 0 and 5),
    fstart          date,
    nalog_reg_date  date,
    reg_date        date,
    sel_kind        smallint check (sel_kind between 0 and 3),
    id              uuid not null,
    low_address_id  uuid,
    post_address_id uuid,
    foms            varchar(64),
    fss             varchar(64),
    inn             varchar(64),
    kpp             varchar(64),
    low_kladr       varchar(64),
    nalog_code      varchar(64),
    ogrn            varchar(64),
    okato           varchar(64),
    okdp            varchar(64),
    okfs            varchar(64),
    okopf           varchar(64),
    okpo            varchar(64),
    okved           varchar(64),
    pfr             varchar(64),
    post_kladr      varchar(64),
    furl            varchar(120),
    country         varchar(512),
    nalog_name      varchar(512),
    strictname      varchar(512),
    fullname        varchar(2000),
    low_address     varchar(2000),
    post_address    varchar(2000),
    primary key (id)
);

create table business_ai.orgdep
(
    direction    smallint check (direction between 0 and 2),
    organization uuid         not null,
    parent_org   uuid,
    dtype        varchar(31)  not null,
    fname        varchar(512) not null,
    parent_name  varchar(512),
    place        varchar(512),
    primary key (organization, fname)
);

create table business_ai.orglink
(
    enddate   date,
    fkind     smallint not null check (fkind between 0 and 9),
    startdate date,
    dest_id   uuid     not null,
    source_id uuid     not null,
    primary key (fkind, dest_id, source_id)
);

create table business_ai.prompts
(
    ai_provider smallint check (ai_provider between 0 and 0),
    kind        smallint check (kind between 0 and 2),
    id          uuid not null,
    fcontent    text,
    primary key (id)
);

create table business_ai.publication_assortment
(
    priority    BIGINT,
    assortment  uuid not null,
    publication VARCHAR(255) NOT NULL,
    CONSTRAINT publication_assortment_pkey PRIMARY KEY (assortment, publication),
    CONSTRAINT fkdwrhq4sr5wmypwqhyt6yh02s9 FOREIGN KEY (assortment) REFERENCES business_ai.assortment (id) ON DELETE NO ACTION
);

create table business_ai.publication_assortments
(
    assortments_id uuid not null,
    publication_plan_fname varchar(512) not null,
    CONSTRAINT fknp8wiy34wpug94pivq65o48bq FOREIGN KEY (publication_plan_fname)
    REFERENCES business_ai.ai_plans (fname) ON DELETE NO ACTION,
    CONSTRAINT fkpx7051xohai0pfsgng4t73opw FOREIGN KEY (assortments_id)
    REFERENCES business_ai.assortment (id) ON DELETE NO ACTION
);

create table business_ai.publication_images
(
    publications_created_at      timestamp(6) not null,
    publications_organization_id uuid         not null,
    images                       varchar(512)
);

create table business_ai.publication_platform
(
    created_at      timestamp(6) not null,
    publicated_at   timestamp(6),
    organization_id uuid         not null,
    platform        varchar(512) not null,
    primary key (created_at, organization_id, platform)
);

create table business_ai.publications
(
    fstate          smallint check (fstate between 0 and 1),
    created_at      timestamp(6) not null,
    assortment_id   uuid,
    organization_id uuid         not null,
    prompt_id       uuid,
    fcontent        text,
    primary key (created_at, organization_id)
);

create table business_ai.user_agent
(
    id          uuid not null,
    user_id     uuid,
    fname       varchar(512),
    description text,
    primary key (id)
);

create table business_ai.userinfo
(
    birthday     date,
    active_until timestamp(6),
    main_phone   varchar(15),
    id           uuid        not null,
    dtype        varchar(31) not null,
    fname        varchar(512),
    main_email   varchar(512),
    patronymic   varchar(512),
    surname      varchar(512),
    primary key (id)
);

create table business_ai.userrole
(
    parent      varchar(512),
    rolename    varchar(512) not null,
    app_name    varchar(255) not null,
    description text,
    primary key (rolename, app_name)
);

create table business_ai.userroles
(
    user_id   uuid         not null,
    role_name varchar(512) not null,
    app_name  varchar(255) not null
);

create index IDX3uug4m825x5yg2ja2fd7nam0i
    on business_ai.assortment (manufacturer, article);

create index IDX1sbniwes6ldifn0fhtjsteish
    on business_ai.assortment (manufacturer, fname);

create index IDXa3kia7hwq7hl57vvoyoglvw3i
    on business_ai.assortment (barcode);

create index IDXlg3ch87cdf9mdtt3mvjac5w9y
    on business_ai.organization (strictname);

create index IDXa51or4dy0lx5hhplfrkjlf5rg
    on business_ai.organization (fullname);

create index PUBLICATION_STATE_FIND_UK
    on business_ai.publication_platform (platform, publicated_at);

alter table if exists business_ai.ai_plans
    add constraint FKd5d8h24llspovmkbyc0jljka
        foreign key (prompt_id)
            references business_ai.prompts;

alter table if exists business_ai.ass_analog
    add constraint FKea7pafkssuiq1vpq6qt5fja64
        foreign key (analogies_id)
            references business_ai.assortment;

alter table if exists business_ai.ass_analog
    add constraint FKgg4viu1mywrlmu9klnpm0rfru
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.ass_attach
    add constraint FKkn2je8j14039gldnokgumgf3m
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.ass_image
    add constraint FKe0c0bdlkwyptxqwbj20q9y7pw
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.ass_props
    add constraint FK5ofr82uexg7xfot06ikf7qo78
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.assortment
    add constraint FKqd2hmf0ckxofhgcijuejqhbyg
        foreign key (issuer_id)
            references business_ai.organization;

alter table if exists business_ai.assortment
    add constraint FK834m0bn1hq6onf9a6ucn4ulp8
        foreign key (manufacturer)
            references business_ai.organization;

alter table if exists business_ai.auth_info
    add constraint FKn9u1dxs5o8bi98e9225x0tkru
        foreign key (application)
            references business_ai.application;

alter table if exists business_ai.auth_info
    add constraint FKbdw1u32c378ykxgbenc1ee1hl
        foreign key (user_id)
            references business_ai.userinfo;

alter table if exists business_ai.auth_locate
    add constraint FKacl7nv89hu8mhlxqbs2wgjbyx
        foreign key (user_id)
            references business_ai.userinfo;

alter table if exists business_ai.bank_contact
    add constraint FKqyt5bjayui4ii1j9dq1mku5dr
        foreign key (bank_info_bik, bank_info_fname)
            references business_ai.bank;

alter table if exists business_ai.bank_rekv
    add constraint FK8qgnudyx8obqt0wm00egjiwir
        foreign key (bik, bank_name)
            references business_ai.bank;

alter table if exists business_ai.bank_rekv
    add constraint FK30ox3l90pbvl55nbulnyu0gjw
        foreign key (seller_id)
            references business_ai.organization;

alter table if exists business_ai.communities
    add constraint FKlog829lyn6io63nw2r6y5pro5
        foreign key (community)
            references business_ai.community;

alter table if exists business_ai.communities
    add constraint FKr7s1g989fjw43ygr1sdwv4cfj
        foreign key (user_id)
            references business_ai.userinfo;

alter table if exists business_ai.community
    add constraint FKj9959aqulc0k6iyjr9q8xoenp
        foreign key (fapp)
            references business_ai.application;

alter table if exists business_ai.cust_requests
    add constraint FKpfn9a9g7rx1rkvpui12bcl5hq
        foreign key (organization_id)
            references business_ai.organization;

alter table if exists business_ai.cust_requests
    add constraint FKmkkcdbmvjg23c5hhl5u4f8jka
        foreign key (prompt_id)
            references business_ai.prompts;

alter table if exists business_ai.image_description
    add constraint FKjfvh5ubb5y6vfqfq6fkmk9skn
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.image_description
    add constraint FKjdo3s670oqrn8rq9mfaoxokb4
        foreign key (prompt_id)
            references business_ai.prompts;

alter table if exists business_ai.org_ai_plans
    add constraint FKlaky1htb0wrdsagl2r0o0vqit
        foreign key (org_id)
            references business_ai.organization;

alter table if exists business_ai.org_ai_plans
    add constraint FK92nkri9u1usjt48rmfuqonjqt
        foreign key (plan_name)
            references business_ai.ai_plans;

alter table if exists business_ai.org_attachment
    add constraint FK3qrjuuer0q2y6jsnid4keqshd
        foreign key (organization_id)
            references business_ai.organization;

alter table if exists business_ai.org_contact
    add constraint FK4qfspuoky1a6uq45purn764k1
        foreign key (organization_id)
            references business_ai.organization;

alter table if exists business_ai.org_director
    add constraint FKfomw1e4pvykiygcqmf24kvhv7
        foreign key (organization_id)
            references business_ai.organization;

alter table if exists business_ai.org_group
    add constraint FKaiorghg868uwtmlijjqxgivt9
        foreign key (org_id)
            references business_ai.organization;

alter table if exists business_ai.org_license
    add constraint FKt7ruvfi1s78pgwqw3or702ghn
        foreign key (issuer)
            references business_ai.organization;

alter table if exists business_ai.org_license
    add constraint FKakpm1u1wica95nq0j1nimiguu
        foreign key (licentiate)
            references business_ai.organization;

alter table if exists business_ai.org_link_prop
    add constraint FKa45xc3cbu182ivb8l4508fggy
        foreign key (fkind, dest_id, source_id)
            references business_ai.orglink;

alter table if exists business_ai.org_prop
    add constraint FKdbuqc27svl5qksb602tne4eeg
        foreign key (org_id)
            references business_ai.organization;

alter table if exists business_ai.orgdep
    add constraint FKil0rqc9u6aopxq0mc7s7e288e
        foreign key (organization)
            references business_ai.organization;

alter table if exists business_ai.orgdep
    add constraint FKfwnjakl3xfc9t4ruvnq9h83n
        foreign key (parent_org, parent_name)
            references business_ai.orgdep;

alter table if exists business_ai.orglink
    add constraint FK35ub0k0v5w71gjv97l987bhmd
        foreign key (dest_id)
            references business_ai.organization;

alter table if exists business_ai.orglink
    add constraint FK1xufcac219p8sqh5oefoien6g
        foreign key (source_id)
            references business_ai.organization;

alter table if exists business_ai.publication_images
    add constraint FK2fntge3axkwbwvisqli24halr
        foreign key (publications_created_at, publications_organization_id)
            references business_ai.publications;

alter table if exists business_ai.publication_platform
    add constraint FKbcyrg29onneiov39fthj3ujty
        foreign key (created_at, organization_id)
            references business_ai.publications;

alter table if exists business_ai.publications
    add constraint FK8txf2b0seae0rxe78ey1wkenj
        foreign key (organization_id)
            references business_ai.organization;

alter table if exists business_ai.publications
    add constraint FKopbdr8vpdw9jy0mfjeu765bwq
        foreign key (assortment_id)
            references business_ai.assortment;

alter table if exists business_ai.publications
    add constraint FKro2wvd7hgi9t8bdlg6g4rgo71
        foreign key (prompt_id)
            references business_ai.prompts;

alter table if exists business_ai.userrole
    add constraint FK191ecfjo4r8y65pldepfb1beh
        foreign key (app_name)
            references business_ai.application;

alter table if exists business_ai.userrole
    add constraint FK27l0kvt6ajyulkk78fl6dr8fn
        foreign key (parent, app_name)
            references business_ai.userrole;

alter table if exists business_ai.userroles
    add constraint FK3thepxv9n6ifvyuru6sghp3wj
        foreign key (role_name, app_name)
            references business_ai.userrole;

alter table if exists business_ai.userroles
    add constraint FKo74l672fgnrjpdahxd6hs0akj
        foreign key (user_id)
            references business_ai.userinfo;

insert into business_ai.application(fgroup, fname, description) values ('for test only', 'blank',
           'Шаблон приложений с интерфейсом пользователя на nuxt-е');

insert into business_ai.application(fgroup, fname, description) values ('business', 'business-ai',
           'Приложение для продвижения бизнеса с использованием искусственного интеллекта');

insert into business_ai.community(status, fapp, fname)
values (4, 'business-ai', 'Технологии третьего тысячелетия');

insert into business_ai.organization(fkind, sel_kind, id, inn, ogrn, country, strictname, fullname)
values (3, 2, 'f830339d-2a63-4ceb-994b-be90fa430f27', '7449156221', '1257400002287',
        'Российская федерация', 'Технологии третьего тысячелетия',
        'Общество с Ограниченной Ответственностью "Технологии третьего тысячелетия"');

insert into business_ai.assortment(id, manufacturer, fname, description)
values ('2c26bb9c-e91c-4735-b01b-5ddcc1762885', 'f830339d-2a63-4ceb-994b-be90fa430f27',
        'SEO-продвижение сайта Заказчика', 'Что входит: <br>Сбор и кластеризация семантического ядра ' ||
        '<br>Технический SEO-аудит и исправление ошибок<br>Оптимизация структуры сайта<br>Написание и публикация SEO-статей ' ||
        '<br>Внутренняя перелинковка, настройка мета-тегов<br>Аналитика и отчёты по росту позиций<br>Выгоды:<br>' ||
        'Привлечение трафика без бюджета на рекламу<br>Лиды с высоким доверием (люди сами ищут услугу)<br>' ||
        'Эффект накапливается и работает в долгую<br>Увеличение узнаваемости бренда');

insert into business_ai.assortment(id, manufacturer, fname, description)
values ('e33a9eab-86ac-4f68-9e3b-599a96ab83db', 'f830339d-2a63-4ceb-994b-be90fa430f27',
        'Ведение Телеграм-канала Заказчика', 'Что входит: <br>Разработка контент-стратегии ' ||
        '(рубрики, tone of voice, частота публикаций)<br>Оформление канала: описание, аватар, закреп<br>' ||
        'Создание контента: тексты, сторис, баннеры<br>Подбор ключевых тем с учётом интересов целевой аудитории<br>' ||
        'Настройка автопостинга (если нужно)<br>Привлечение подписчиков через рекламу и взаимопиар (опционально)<br>' ||
        'Аналитика: вовлечённость, рост подписчиков, реакции<br>Выгоды:<br>Построение сообщества вокруг бренда<br>' ||
        'Прямой контакт с целевой аудиторией<br>Повышение доверия и лояльности<br>Канал — как лендинг: ' ||
        'можно сразу продавать<br>Возможность тестировать гипотезы и продукты');

insert into business_ai.assortment(id, manufacturer, fname, description)
values ('e6567355-b9e3-4491-b0cd-0ed950f68ab8', 'f830339d-2a63-4ceb-994b-be90fa430f27',
        'Ведение личного кабинета Заказчика в Яндекс-Бизнес', 'Что входит:<br>Оптимизация профиля ' ||
        '(первоначальное заполнение, уникальные торговые предложения, ключи)<br>Добавление товаров / услуг<br>' ||
        'Настройка связи с сайтом, телефоном, мессенджерами<br>Аналитика: охваты, переходы, видимость<br>' ||
        'Регулярные посты с фото, предложениями, новостными публикациями<br>Сбор и обработка отзывов<br>' ||
        'Ответы на отзывы и вопросы пользователей с помощью искусственного интеллекта<br>Выгоды:<br>' ||
        'Попадание в топ локальной выдачи Яндекса<br>Дополнительный канал без бюджета на рекламу<br>' ||
        'Повышение доверия через отзывы<br>Увеличение входящих звонков и заявок');
