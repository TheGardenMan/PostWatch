-- Commands related to YT

create table yt_table(hash_id char(16) primary key,time_of_upload timestamptz not null,tags text[] not null);
insert into yt_table(hash_id,time_of_upload,tags) values('asasasasasasasas',current_timestamp,'{"wonders","are","done","in","rooms"}');
