# Demo Export Files

These files are prepared outputs for the final demo video.

- `oncoreconcile-fhir-PT-DEMO-001.json` - expanded FHIR R4 Bundle prototype for the synthetic `PT-DEMO-001` patient journey.
- `oncoreconcile-omop-PT-DEMO-001.json` - expanded OMOP CDM v5.4-oriented records for the synthetic `PT-DEMO-001` patient journey.

They were generated from the local FastAPI endpoints:

- `POST /enterprise/export/fhir/PT-DEMO-001`
- `POST /enterprise/export/omop/PT-DEMO-001`

FHIR and OMOP exports are prototype outputs for interoperability demonstration and require implementation-specific validation before production use.
