-- Khafeefa admin dashboard migration
-- Run on the production PostgreSQL (pgweb / dbgate / psql) once.
-- Adds analytic columns on orders + creates the clicks table.
-- Re-running is safe; every statement is idempotent.

BEGIN;

-- ---------------------------------------------------------------
-- ORDERS: new analytic / admin columns
-- ---------------------------------------------------------------
ALTER TABLE orders
    ADD COLUMN IF NOT EXISTS session_id        VARCHAR,
    ADD COLUMN IF NOT EXISTS country_code      VARCHAR(2),
    ADD COLUMN IF NOT EXISTS is_vpn            BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS is_valid_traffic  BOOLEAN DEFAULT TRUE,
    ADD COLUMN IF NOT EXISTS admin_notes       TEXT;

CREATE INDEX IF NOT EXISTS ix_orders_session_id        ON orders (session_id);
CREATE INDEX IF NOT EXISTS ix_orders_country_code      ON orders (country_code);
CREATE INDEX IF NOT EXISTS ix_orders_is_valid_traffic  ON orders (is_valid_traffic);
CREATE INDEX IF NOT EXISTS ix_orders_created_at        ON orders (created_at);
CREATE INDEX IF NOT EXISTS ix_orders_created_at_valid  ON orders (created_at, is_valid_traffic);

-- ---------------------------------------------------------------
-- CLICKS: page-view / landing event table for conversion-rate math
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clicks (
    id                  UUID PRIMARY KEY,
    session_id          VARCHAR NOT NULL,
    visitor_id          VARCHAR,
    client_ip           VARCHAR,
    user_agent          TEXT,
    referrer            TEXT,
    landing_page_url    TEXT,
    page_path           VARCHAR,
    country_code        VARCHAR(2),
    is_vpn              BOOLEAN DEFAULT FALSE,
    is_valid_traffic    BOOLEAN DEFAULT TRUE,
    maxmind_risk_score  NUMERIC(5, 2),
    utm_source          VARCHAR,
    utm_medium          VARCHAR,
    utm_campaign        VARCHAR,
    utm_content         VARCHAR,
    utm_term            VARCHAR,
    fbp                 VARCHAR,
    fbc                 VARCHAR,
    ttclid              VARCHAR,
    sc_click_id         VARCHAR,
    created_at          TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_clicks_session_id        ON clicks (session_id);
CREATE INDEX IF NOT EXISTS ix_clicks_visitor_id        ON clicks (visitor_id);
CREATE INDEX IF NOT EXISTS ix_clicks_country_code      ON clicks (country_code);
CREATE INDEX IF NOT EXISTS ix_clicks_is_vpn            ON clicks (is_vpn);
CREATE INDEX IF NOT EXISTS ix_clicks_is_valid_traffic  ON clicks (is_valid_traffic);
CREATE INDEX IF NOT EXISTS ix_clicks_utm_source        ON clicks (utm_source);
CREATE INDEX IF NOT EXISTS ix_clicks_utm_campaign      ON clicks (utm_campaign);
CREATE INDEX IF NOT EXISTS ix_clicks_created_at        ON clicks (created_at);
CREATE INDEX IF NOT EXISTS ix_clicks_created_at_valid  ON clicks (created_at, is_valid_traffic);

-- ---------------------------------------------------------------
-- Tell Alembic this version is applied (so a future redeploy does
-- not try to run the same migration again).
-- If you do not use Alembic, this UPDATE is a no-op.
-- ---------------------------------------------------------------
UPDATE alembic_version
   SET version_num = 'add_admin_dashboard'
 WHERE EXISTS (SELECT 1 FROM alembic_version);

COMMIT;
