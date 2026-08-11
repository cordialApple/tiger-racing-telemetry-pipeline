CREATE TABLE IF NOT EXISTS ingestion_source (
    packet_id   TEXT NOT NULL REFERENCES ingestion_log(packet_id) ON DELETE CASCADE,
    source_path TEXT NOT NULL,
    seen_at     TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (packet_id, source_path)
);

ALTER TABLE ingestion_source DROP CONSTRAINT IF EXISTS ingestion_source_packet_id_fkey;

ALTER TABLE ingestion_source ADD CONSTRAINT ingestion_source_packet_id_fkey
    FOREIGN KEY (packet_id) REFERENCES ingestion_log(packet_id) ON DELETE CASCADE;
