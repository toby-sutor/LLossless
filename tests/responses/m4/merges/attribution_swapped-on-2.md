The Vandrell Relay listens on port 8443.
The health check path is /healthz.

Unresolved: the read timeout.
source_a.md states that the read timeout is 30 seconds.
source_b.md states that the read timeout is 60 seconds.
The sources disagree and this merge does not choose between them.