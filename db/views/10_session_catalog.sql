DROP VIEW IF EXISTS v_session_catalog CASCADE;

CREATE OR REPLACE VIEW v_session_catalog AS
SELECT s.session_id, s.source_file, s.platform, s.event, s.vehicle, s.racer,
       s.championship, s.session_name, s.comment, s.started_at, s.duration_s,
       s.sample_rate_hz, il.reading_count, il.loaded_at
FROM sessions s
LEFT JOIN ingestion_log il USING (session_id);
