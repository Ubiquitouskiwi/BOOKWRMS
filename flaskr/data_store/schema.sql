create table if not exists author (
    id serial primary key,
    first_name varchar(75) not null,
    middle_name varchar(75),
    last_name varchar(75) not null,
    olid varchar(20),
    created_at timestamp not null default CURRENT_TIMESTAMP,
    deleted bool not null default false
);

create table if not exists book (
    id serial primary key,
    title varchar(100) not null,
    author_id serial not null,
    isbn int8 unique not null,
    illustration_url varchar(255) not null,
    olid varchar(20),
    created_at timestamp not null default CURRENT_TIMESTAMP,
    deleted bool not null default false,
    foreign key (author_id) references author (id)
);

create table if not exists account (
    id serial primary key,
    first_name varchar(75) not null,
    last_name varchar(75) not null,
    email varchar(255) unique not null,
    is_admin bool not null,
    created_at timestamp not null default CURRENT_TIMESTAMP,
    deleted bool not null default false
);

create table if not exists login (
    id serial primary key,
    email varchar(255) unique not null,
    pass varchar(255) not null,
    created_at timestamp not null default CURRENT_TIMESTAMP,
    deleted bool not null default false
);

create table if not exists checkout_log (
    id serial primary key,
    book_id serial not null,
    patron_name varchar(100) not null,
    checkout_date timestamp not null,
    checkout_duration smallint not null,
    checkin_date timestamp,
    renew_count smallint not null default 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    foreign key (book_id) references book (id)
);

create table if not exists invite_code (
    id serial primary key,
    code varchar(6) not null,
    used bool not null default false,
    user_email varchar(255),
    used_date timestamp,
    created_by varchar(255) NOT NULL default 'system',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

create table if not exists user_book_tag (
    id serial primary key,
    book_id serial not null,
    user_id serial not null,
    tag_value varchar(50) not null,
    tag_color varchar(7) not null default '#000000',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT false,
    foreign key (book_id) references book (id),
    foreign key (user_id) references account (id)
);