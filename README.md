# Promprint Database
A django-based front end for editing and interacting with the [promprint](https://cordis.europa.eu/project/id/101163126) database.

This is currently a work in progress.

Promprint will explore rejects of legal deposit in 19th-century UK libraries. The database enables this by storing and comparing separate tables of data:

1) A reference table containing the title, author and date of all publications listed in the registers of the Stationer's Hall under the copyright act, for a set of dates that is the subject of this research project

2) A table for each of the UK legal deposit libraries, containing all publications (and associated metadata) received by those libraries during the years covered by the registers of the Stationer's Hall

The front end will enable exploration of the data and metadata, allowing us to find gaps in the legal deposit record when referenced to the Stationer's Hall register.

## Installation
The project will be installed using [`uv`](https://github.com/astral-sh/uv), and the data will be published in a portable format so that the whole system can be explored by other researchers. Documentation to follow.

## Tasks
- [ ] Create the basic table structure for the Stationer's Hall data, allowing us to start populating that table via both manual and automated transcription of the digitised copies of the registers.
- [ ] Once legal deposit data from the British Library is Received, build out the corresponding table based on their metadata structure
- [ ] Explore convenient ways to match data (fuzzy search?) and to build/join new tables that can help research explore themes behind the gaps in the data

