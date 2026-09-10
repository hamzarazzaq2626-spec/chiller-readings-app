CREATE TABLE IF NOT EXISTS plant_readings (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  reading_at TIMESTAMPTZ NOT NULL,
  ambient_temp_c NUMERIC,
  primary_motors_running INTEGER,
  secondary_motors_running INTEGER,
  chillers_running INTEGER,
  compressors_running INTEGER,
  total_power_kw NUMERIC,
  total_refrigeration_ton NUMERIC,
  primary_in_bar NUMERIC,
  primary_out_bar NUMERIC,
  secondary_in_bar NUMERIC,
  secondary_out_bar NUMERIC,
  return_temp_c NUMERIC,
  supply_temp_c NUMERIC,
  delta_t_c NUMERIC,
  motor_load_kw NUMERIC,
  chiller_load_kw NUMERIC,
  chiller_efficiency_kw_tr NUMERIC,
  plant_efficiency_kw_tr NUMERIC,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chiller_readings (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  reading_at TIMESTAMPTZ NOT NULL,
  chiller_number TEXT NOT NULL,
  is_on BOOLEAN NOT NULL DEFAULT TRUE,
  compressors_running INTEGER,
  load_percent NUMERIC,
  ewt_c NUMERIC,
  lwt_c NUMERIC,
  flow NUMERIC,
  calibration_1 NUMERIC,
  power_kw NUMERIC,
  delta_t_c NUMERIC,
  far NUMERIC,
  calibration_2 NUMERIC,
  total_tr NUMERIC,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS plant_readings_reading_at_idx ON plant_readings (reading_at DESC);
CREATE INDEX IF NOT EXISTS chiller_readings_reading_at_idx ON chiller_readings (reading_at DESC);
