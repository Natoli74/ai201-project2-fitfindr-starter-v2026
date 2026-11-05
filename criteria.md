# Shape B Acceptance Criteria

These criteria define objective, repeatable checks for the failure-hardening
extension and the existing FitFindr execution path.

## 1. Timeout Fallback (Extension)

When an API or external service call is forced to exceed the strict 5-second
timeout, **5 of 5 runs** must return a graceful fallback JSON message without
raising a traceback or crashing the caller.

**Numerical target:** 5/5 successful fallback responses; 0/5 traceback
responses.

**Rationale:** Prevents UI hangs and unhandled exception tracebacks when a
remote model or retrieval service stops responding.

## 2. Rate Limit Retry Backoff (Extension)

Under simulated HTTP 429 errors, the retry decorator must apply exponential
backoff and successfully resolve the operation on retry in **3 of 3
attempted scenarios**.

**Numerical target:** 3/3 scenarios succeed after a retry; each scenario
records at least 1 retry and uses backoff delays of
`1.5 * 2^attempt` seconds.

**Rationale:** Prevents transient rate spikes from dropping otherwise valid
queries while keeping retry behavior bounded and measurable.

## 3. Empty / Invalid Input (Extension)

For an empty string and malformed JSON payloads sent to `POST /ask`, the
service must return an HTTP 400-equivalent response in **5 of 5 runs** for
each invalid-input case, with a structured error message and no traceback.

**Numerical target:** 10/10 invalid-input requests return status 400; 0/10
return status 500 or an unhandled exception.

**Rationale:** Ensures edge-case inputs fail fast at the HTTP boundary instead
of entering the agent loop or producing confusing downstream failures.

## 4. Execution Latency

Standard successful queries that find at least one listing must complete with
an average latency under **3.5 seconds across 3 full trial batches**.

**Numerical target:** Run 3 batches of 3 matching queries (9 total runs);
each batch average must be `< 3500 ms`.

**Rationale:** Maintains an acceptable user response time while measuring
normal end-to-end search, model, and fit-card execution rather than a single
best-case request.

## 5. Structured Log Persistence

**100% of execution runs** must append exactly one valid JSON object to
`runtime.log` containing `timestamp`, `input`, `output`, `status`,
`duration_ms`, and either `cost_usd` or `tokens_used`.

**Numerical target:** For a 10-run measurement, 10/10 new lines parse as JSON,
10/10 contain all six required fields, and 10/10 have status values from
`SUCCESS`, `TIMEOUT`, `RATE_LIMIT`, or `ERROR`.

**Rationale:** Enables operational auditability for both successful requests
and caught failures, including measured duration and model usage.
