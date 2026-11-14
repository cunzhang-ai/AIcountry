# An upstream update and the work left after technical recovery

On 19 July 2024 CrowdStrike issued a security content configuration
update for its Windows sensor. Its preliminary account gives a
release time of 04:09 UTC and reversion at 05:27 UTC, a window of
78 minutes. The vendor scopes exposure to qualifying online Windows
hosts that received the update. Its subsequent root-cause summary
describes an input mismatch. The sensor expected 20 fields and
received 21, leading to an out-of-bounds read and system crash.
This was a configuration compatibility failure. It is evidence
about a shared update path rather than evidence that an AI
decision itself failed. [Vendor preliminary account](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/)
· [Vendor root-cause summary](https://www.crowdstrike.com/wp-content/uploads/2024/08/Executive-Summary_Root-Cause-Analysis_Channel-File-291.pdf)

On 19 July NHS England reported disruption to GP practice
appointments and patient records and described paper records,
handwritten prescriptions and ordinary telephone contact among its
continuity measures. Its later assurance report says EMIS Web,
used by 60 percent of general practices, and the Lorenzo patient
record system were affected. The 60 percent is stated use of EMIS
Web, not a measured share of missed care. [NHS initial notice](https://www.england.nhs.uk/2024/07/response-to-global-it-outage/)
· [NHS annual assurance report, paragraph 17](https://www.england.nhs.uk/long-read/annual-eprr-assurance-report-march-2025/)

On 22 July NHS England reported systems online while warning
about possible continuing disruption, particularly appointments
that practices needed to rebook. The 78 minutes describe the
vendor's distribution and reversion interval, not the duration
of an individual outage or a national service restoration.
Technical recovery and overdue or rebooked care are distinct.
The inspected records supply no joined count of missed treatment,
actual service continuity or comparative effects of staged release.
[NHS recovery notice](https://www.england.nhs.uk/2024/07/updated-response-to-global-it-outage-22-july/)

[Source custody and limitations](https://github.com/cunzhang-ai/AIcountry/blob/edition-1/research/2026-11-shared-ai-dependencies-and-safe-changes/sources.md)
