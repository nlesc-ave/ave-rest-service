DROP TABLE IF exists metadata;
CREATE TABLE metadata (
    meta_id integer primary key autoincrement,
    species text not null,
    genome text not null,
    datatype text not null,
    filename text not null
);
