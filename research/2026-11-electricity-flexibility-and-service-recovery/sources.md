# Design474 sources and scope

Energinet's [settlement snapshot](original-sources/ProductionConsumptionSettlement.json)
and [day-ahead price snapshot](original-sources/Elspotprices.json)
are original API responses for 20 January 2025, 16:00 inclusive
to 22:00 exclusive in Danish time, both DK1 and DK2. The
[API guide](https://energidataservice.dk/guides/api-guides)
describes the query conventions. Match hour and area under the
recorded UTC and local times. The selected hours are 16:00 and
19:00 UTC. The exercise is reproducible without a live download.

The [Energinet data catalogue](https://www.energidataservice.dk/Data_catalog_EN.pdf),
printed pages 6 and 10, describes gross consumption from production
and exchange, losses and the electricity-for-heat category.
The [official 2025 market report](https://en.energinet.dk/media/v2fhaaxv/250226-electricity-market-report-2025.pdf),
printed page 16, confirms the 17:00 price of EUR 583.4/MWh in
both Danish bidding zones. These sources do not supply real billed
cost, financial or contractual settlement, local safe load, resource
rights, or received warmth. The reported temporal comparison
establishes neither causation nor the frequency of a joint event.

[Worked recovery and gross cost](../settlement/electricity-flexibility-and-service-recovery/01-a-cheaper-hour-and-a-busier-connection.md)
uses constructed local load, rights, protected heating requirements,
available staff, contract terms and 21:00 price.
[Original grid rules](../country/C09/19/01-operator-and-connection.md)
and [public AI portfolio](../country/C11/09/19-public-ai-portfolio-and-common-inputs.md)
provide the applicable design context.
