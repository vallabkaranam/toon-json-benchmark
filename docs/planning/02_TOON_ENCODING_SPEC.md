# TOON Encoding Specification

## Purpose
Defines a deterministic, lossless mapping between JSON and TOON.

## Structure
A TOON file has:
1. Collection header
2. Schema declaration
3. Data rows

## Collection Header
events[<count>]:

## Schema Declaration
{
  id,
  timestamp,
  service,
  env,
  type,
  status,
  severity,
  source,
  metadata.request_id,
  metadata.user_id,
  metadata.region,
  metadata.retry_count,
  metadata.latency_ms,
  metadata.tags,
  message
}

## Row Format
Comma-separated values in schema order.

## Value Rules
- Strings unquoted unless spaces/commas exist
- Numbers raw
- Arrays as [a,b,c]
- No nulls

## Example
events[200]:
{id,timestamp,service,env,type,status,severity,source,metadata.request_id,metadata.user_id,metadata.region,metadata.retry_count,metadata.latency_ms,metadata.tags,message}
evt_0142,2025-01-12T14:32:10Z,billing-service,prod,payment,failed,4,worker-3,req_8f31a,user_8341,us-east,2,1840,[payment,critical],"Payment authorization failed after retry."

## Guarantees
- Lossless JSON roundtrip
- Fixed ordering
- Deterministic output
