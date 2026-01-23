Input: Company name and primary listing market or country (if available)
Output: A structured “Board Term and Renewal Timetable” covering


Supervisory Board members: term end date, next reelection or renewal point, relevant AGM cycle, and supporting source references


Executive Board members: contract end date or disclosed renewal horizon where available, and supporting source references


Data confidence flags (Confirmed, Inferred, Not disclosed) with a short rationale for each


A short BD oriented “Implications” section highlighting upcoming term cliffs and concentrated renewal windows


Method


Start with the official company investor relations and governance pages to identify current board composition and governance framework


Locate and review the most relevant official documents, prioritizing
a. AGM and proxy materials (including agenda items and election or reelection proposals)
b. Annual report and corporate governance report
c. Articles of association or governance charter, if needed to interpret term length conventions
d. Press releases on appointments or contract extensions, especially for executive directors


Extract for each individual the explicit term end date or the AGM year when the mandate ends


If sources provide only an election year or a maximum term length, infer the likely end window using documented rules and clearly label it as “Inferred”


If no official disclosure is found after checking the core sources above, mark the field “Not disclosed” and list the sources searched


Formatting requirements


Provide results in a table with one row per board member


Include a “Source” column that names the document and date, plus where to find it (for example, Annual Report 2024, Corporate Governance section; AGM Invitation 2025, agenda item on elections)


Separate Supervisory Board and Executive Board sections


Include a final “Next 12 to 24 months watchlist” summary, sorted by soonest upcoming end or reelection date


Scope and constraints


Use only official company sources and clearly attributable public disclosures


Do not use paid databases as the primary source for term end dates


Prefer primary documents over secondary commentary


Be explicit about uncertainty and do not fabricate missing dates


Ensure outputs are suitable for business development trigger analysis and smart pack inclusion


Future enhancement hooks


Support batch runs for an index set (for example, all DAX40 companies) with standardized outputs


Add an optional relationship overlay step: if internal relationship data is provided, identify relevant connection holders (for example, NomCo Chair relationships) and produce a notification ready summary


Extend the trigger logic to highlight patterns such as multiple simultaneous expirations, governance driven refresh cycles, and committee chair transitions
