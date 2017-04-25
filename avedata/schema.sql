DROP TABLE IF exists metadata;
CREATE TABLE metadata (
    meta_id integer primary key autoincrement,
    species text not null,
    genome text not null,
    datatype text not null,
    filename text not null
);
DROP TABLE IF exists features;
CREATE TABLE features (
    meta_id integer not null,
    name text not null,
    chromosome text not null,
    start integer not null,
    end integer not null
);
CREATE INDEX IF NOT EXISTS features_name_i ON features (name);
