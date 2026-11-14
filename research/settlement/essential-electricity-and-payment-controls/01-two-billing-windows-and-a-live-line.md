# Two billing windows and a live line

This constructed case tests [EPC01–EPC08](../../country/C09/19/05-essential-electricity-and-payment-controls.md).
A tenant needs four units of electricity in each of two successive useful
windows for essential equipment and safe temperature. Assume each unit costs
one credit. The tenant can pay two credits each window before the useful
deadline. A shared prepayment account shows six credits of disputed debt
attributed to a prior occupant. The case does not treat that debt as a valid
claim against the tenant.

In the first window two credits of lawful assistance reach the current
service. In the second only one of two planned credits settles in time.
One more settles later. The live network and a qualified continuation route
can deliver four units without relying on timely billing confirmation.

| Path | First-window power | Second-window power | Cash and liability |
|---|---:|---:|---|
| Allow the meter to take two current credits against the prior account's debt in the first window, then restrict supply by balance | 2 of 4 | At most 3 of 4 even without another deduction | First-window diversion is unauthorized in this case |
| Keep current payments separate but restrict supply by balance | 4 of 4 | 3 of 4 | The late assistance cannot meet the original deadline |
| Protect actual current supply and reconcile separate payments | 4 of 4 | 4 of 4 | One credit of authorized service cost remains unsettled at the second deadline |

Under the selected rule the prior-account deduction is disallowed. The
second window records four units received and only three credits settled.
The remaining one follows its own lawful funding and review route. Later
settlement closes that amount, without changing its original cash timing.
It cannot be charged again or used to deny the next protected interval.

If the feeder is physically unavailable in the second window, settled money
and the billing continuation arrangement deliver zero from the grid. A
qualified, independent alternate that can serve four units in time changes
that result. A backup sharing the failed line or arriving after the deadline
does not. Any separately incurred backup cost follows its own source and
cannot be inferred from the four ordinary service credits.

The numbers are assumptions. The comparison tests separate payment, control
and physical service conditions. It supplies no local cost, safety finding,
medical need or actual availability. [Reproduction](verify-electricity-controls.py).
