# A cheaper hour can have less room for a new public load

*Design474 · Observed Danish hourly statistics and a separate constructed
public operating decision.*

## Two hours in the same official series

On 20 January 2025 Energinet identified 17:00 as the day's highest
day-ahead spot price and the highest for both Danish bidding zones
in 2025. Join its electricity settlement and historical prices by
UTC hour and bidding zone. Sum DK1 and DK2 only for each settlement
measure. The hourly records mark the beginning of the interval.

| Danish local time (CET) | Gross electricity, both zones, MWh | Electricity for heat, both zones, MWh | DK1 and DK2 spot, DKK/MWh |
|---|---:|---:|---:|
| 17:00 | 5,774.251800 | 154.078391 | 4,352.689941 |
| 20:00 | 5,048.627654 | 210.693113 | 1,641.400024 |

Gross electricity is Energinet's settlement calculation from
production and exchange. The reported power-to-heat field covers
primarily electric boilers. It is a separate view of use and is
not added to gross. The lower national gross figure at 20:00
coincides with a higher recorded heat figure. Neither gives the
connection's available MW, household warmth, interchange capacity
during a local failure or an individual bill.

Ten MWh at those respective spot prices would cost DKK 43,526.90
and 16,414.00, a modeled energy-only difference of DKK 27,112.90.
The arithmetic assumes identical pass-through and no fees,
losses, hedge, obligations on the earlier order, or change in
the price caused by moving the load. No actual purchase or saving
is measured.
[Original snapshots, definitions and sources](../../2026-11-electricity-flexibility-and-service-recovery/sources.md).

## Compare actual public choices in a qualified local window

The following connection, work, service and funding terms are
fictional. A scheduled optional AI batch needs 10 MWh in one hour
or independently qualified checkpoints at 4 and 6 MWh. Its latest
useful completion is 22:00. A paid ordinary route already protects
the underlying access, including an independent route for urgent
requests. Report the extra work that would wait without the batch.
An essential heating recovery needs 8 MW at 20:00 on the same
connection to keep occupied homes safe. Assume the competent
operator has verified the following usable MW throughout each
one-hour interval, before any incremental heat and batch demand.
This includes the applicable start and ramp limits in the fixture.

| Window | Verified headroom before both additions, MW | Heating recovery, MW | Room for optional work, MW |
|---|---:|---:|---:|
| 17:00–18:00 | 10 | 0 | 10 |
| 20:00–21:00 | 12 | 8 | 4 |
| 21:00–22:00 | 6 | 0 | 6 |

A full shift to 20:00 exceeds the actual limit by 6 MW. If the
21:00 block and verified checkpoints qualify, the split can finish
at the deadline with actual restart energy included in the stated
scope. If they fail, count neither the missing block nor the
associated later service as covered. If all work must run at 20:00,
select the funded original 17:00 alternative before it expires,
or preserve staffed delivery without the optional batch. Actual
safety, accepting staff, price terms and independent access still
govern. No low price allocates the connection to an AI operator.

For the split, test a constructed 21:00 payable energy price of
DKK 2,000/MWh, no fuel or other fees, and a DKK 50,000 cap
after standing work. This produces a gross purchase of
DKK 18,565.60 if the earlier purchase never bound. A separate
version assumes the earlier energy is already payable under its
terms, no offset clears by the cutoff and paying for it does
not provide usable energy at either later hour. The same split
would use DKK 62,092.50 gross, over the cap by DKK 12,092.50.
The already payable 17:00 block remains available in its actual
scope unless lawfully released. Paying it and running the
qualified original schedule costs DKK 43,526.90 on these terms.
In a real decision also reconcile volume nomination, resale or
credited use, cancellation, settlement and imbalance by due time.
A projected recovery changes no earlier cash bound. A fully
qualified later alternative can be chosen on its actual net
terms and decision, with the protected heat untouched.

Retain operator-approved scheduling and actual public buying on
their own authorities. AI may propose time blocks but cannot
release the connection or the cash. Require safe next-call cover
and report what actually reached households in the recovery window.
Do not claim that heating was lost or capacity constrained in
the observed Danish hours. This result selects a prospective
release rule for separately established local risks.

[Reproduction](verify-flexible-recovery.py)
· [Connection rules](../../country/C09/19/04-large-grid-connections-and-paid-capacity.md)
· [Public AI portfolio](../../country/C11/09/19-public-ai-portfolio-and-common-inputs.md).
