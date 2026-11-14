# Compare service through start, transfer and renewed loss

All quantities here are authored planning assumptions. H0 is the start of
the protected interval after initial loss. Existing qualified ride-through
covers the initial switchover. The protected continuous loads are 3 MW of
clinic, 1 MW of communications and 2 MW of water. The island has 7 MW
of qualified real-power capacity and 24 MWh of usable stored energy at
H0. The water equipment draws 5 MW during an ordinary restart and 2.5 MW
with a qualified staged start. Require 0.5 MW of headroom. The staged start
uses a separate budget of 0.1 MWh from the same store in addition to the
continuous-load approximation. Assume all other electrical safety gates
pass only in cases that meet the stated planning limits.

For this comparison, the clinic and communications require continuous
usable service. An independent treated water buffer is verified to sustain
the water duty through H1. The staged route verifies usable pressure and
water quality before H1. In the bulk-only case, those first three hours
require actual alternate services and the fixture supplies no additional
alternate beyond the water buffer. Independent protected receipt
continues through a transfer. H3 and H5 are candidate times when an
external tie can accept the protected load with 10 MW available. The island
carries the full 6 MW and the tie contributes no credit for the next
half-hour of transfer proving.

| Path | First interval and limiting condition |
|---|---|
| Bulk only, tie at H3 | Clinic and communications are exposed from H0. Water is exposed after H1 until downstream receipt. |
| Local only, ordinary restart | The proposed water restart demands 9 MW in total. Holding it preserves clinic and communications while water has only the verified buffer. |
| Local only, qualified staged restart | Startup demand of 6.5 MW leaves the required 0.5 MW margin. The combined 6 MW load exhausts the store at H3 plus 59 minutes. |
| Combined route, tie at H3 | 6 MW for 3.5 h plus 0.1 MWh consumes 21.1 MWh. Successful transfer leaves 2.9 MWh in the island, equivalent to 29 minutes at 6 MW without another start. |
| Combined route, tie at H5 | 6 MW for 5.5 h plus 0.1 MWh requires 33.1 MWh. The local route is short by 9.1 MWh before verified transfer. |

A renewed 30-minute island call with no recharge and no further start
would need 3 MWh. The H3 path is short by 0.1 MWh even on that favorable
assumption. The portfolio passes the modeled first handoff at H3 and
fails the second call unless a qualified service alternate or additional
owned usable energy is available. The H5 path requires an accepted service
bridge starting before H3 plus 59 minutes. The electrical deficit measures
the full protected load, and any sector substitute has to prove its own
people, time, quality, route and financing.

The numbers are planning bounds. Actual startup and reserve qualification
requires electrical studies and tests for the selected equipment and
operator, including voltage, protection and synchronization. Earlier
handoff, reduced demand under an authorized service plan, greater storage
or verified direct service can each change the result. A live comparison
must reconcile the ordinary crew, source, cash and replenishment schedule
with the [first-budget rules](../../country/C06/65/04-common-failure-and-paid-public-control.md).
