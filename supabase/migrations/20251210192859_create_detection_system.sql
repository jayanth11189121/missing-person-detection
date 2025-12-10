/*
  # Missing Person Detection System Schema

  1. New Tables
    - `missing_persons`
      - `id` (uuid, primary key)
      - `name` (text) - Name of the missing person
      - `description` (text) - Additional details
      - `reference_image_url` (text) - URL to reference image
      - `status` (text) - active, found, inactive
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `detections`
      - `id` (uuid, primary key)
      - `missing_person_id` (uuid, foreign key)
      - `detection_type` (text) - video, webcam, rtsp
      - `confidence_score` (float)
      - `detected_at` (timestamptz)
      - `frame_url` (text) - URL to detected frame image
      - `video_url` (text) - URL to processed video (if applicable)
      - `location_info` (jsonb) - Additional location/metadata
      - `created_at` (timestamptz)
    
    - `detection_reports`
      - `id` (uuid, primary key)
      - `missing_person_id` (uuid, foreign key)
      - `report_data` (jsonb) - Full report data
      - `pdf_url` (text) - URL to generated PDF report
      - `generated_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to manage their data
*/

-- Missing Persons Table
CREATE TABLE IF NOT EXISTS missing_persons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text DEFAULT '',
  reference_image_url text,
  status text DEFAULT 'active' CHECK (status IN ('active', 'found', 'inactive')),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE missing_persons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active missing persons"
  ON missing_persons FOR SELECT
  USING (status = 'active');

CREATE POLICY "Authenticated users can insert missing persons"
  ON missing_persons FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update missing persons"
  ON missing_persons FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete missing persons"
  ON missing_persons FOR DELETE
  TO authenticated
  USING (true);

-- Detections Table
CREATE TABLE IF NOT EXISTS detections (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  missing_person_id uuid REFERENCES missing_persons(id) ON DELETE CASCADE,
  detection_type text NOT NULL CHECK (detection_type IN ('video', 'webcam', 'rtsp')),
  confidence_score float DEFAULT 0.0,
  detected_at timestamptz DEFAULT now(),
  frame_url text,
  video_url text,
  location_info jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE detections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view detections"
  ON detections FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can insert detections"
  ON detections FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update detections"
  ON detections FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete detections"
  ON detections FOR DELETE
  TO authenticated
  USING (true);

-- Detection Reports Table
CREATE TABLE IF NOT EXISTS detection_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  missing_person_id uuid REFERENCES missing_persons(id) ON DELETE CASCADE,
  report_data jsonb DEFAULT '{}',
  pdf_url text,
  generated_at timestamptz DEFAULT now()
);

ALTER TABLE detection_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view reports"
  ON detection_reports FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can insert reports"
  ON detection_reports FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update reports"
  ON detection_reports FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete reports"
  ON detection_reports FOR DELETE
  TO authenticated
  USING (true);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_missing_persons_status ON missing_persons(status);
CREATE INDEX IF NOT EXISTS idx_detections_missing_person_id ON detections(missing_person_id);
CREATE INDEX IF NOT EXISTS idx_detections_detected_at ON detections(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_reports_missing_person_id ON detection_reports(missing_person_id);