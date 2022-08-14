# Fahrplan++

## Introduction

This project intends to provide an "realtime"-Show/Venue Management, managing the performances and providing informations for visitors, crew and casts.

## Concepts
### Events
An Event is an Event, and has an "import url" (JSON from pretalx) to get the planned programme from, as well as a time offset. Normally, an event will run in realtime (time offset 0), however, it can be useful to provide an "simulated" time for rehearsals etc.

### Venue
An Venue is a part of an event, and represents an Stage/Room/etc.

### Performance
An Performance is the Talk, Show, etc. that is shown on the stage, usually by a single (group) of performers.
A Performance has a planned start/duration, and if actually running an actual start/duration.

A performance can be started and stopped manually (and automatically in the future).

Delay and prognosed start/stop are calculated at runtime, and regulary refreshed. This can be used to provide backstage dashboards.