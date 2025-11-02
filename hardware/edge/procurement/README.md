# Procurement & Supplier Outreach — Edge Alpha

This short guide explains how to create purchase orders and perform supplier outreach for the Edge alpha prototype.

1) Prioritize long-lead items
- Jetson modules and cellular modems often have longer lead times. Start quotes with multiple distributors (Digi-Key, Mouser, Arrow, Avnet) and check manufacturer-backed distributor lists.

2) Sample supplier list
- Modules & semiconductors: Digi-Key, Mouser, Arrow, Avnet
- Batteries: Trusted battery specialists or direct vendors (EVE, Winston) — ask for cell datasheets and safety certificates
- Enclosures & connectors: Polycase, OKW, Hammond, Amphenol, TE Connectivity

3) Create a procurement spreadsheet
- Use `hardware/boms/edge_alpha_bom.csv` as the starting BOM. Add columns for: Quote received (Y/N), Supplier contact, Unit price (local currency), MOQ, Lead time (weeks), Incoterms, Last-mile shipping estimate.

4) Regional considerations (ECOWAS)
- Check local import duties, telecom approvals for cellular modules, and availability of carriers supporting eSIM.
- Consider local/regional distributors to reduce shipping times and import complexities.

5) Second sourcing and alternates
- For critical items (compute module, battery cells, cellular modem), identify at least one alternate SKU and supplier in the BOM.

6) QA for received parts
- Request datasheets, RoHS/CE declarations, and sample test certificates for batteries and RF modules.

7) Next steps
- Generate formal RFQs from the BOM and assign the procurement lead.
- Start orders for dev kits and one set of sensors for software/hardware integration.
