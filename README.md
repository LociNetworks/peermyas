# Peer My AS - https://peermyas.net/

Flask based web app to help simplify the peering process. 

Uses PeeringDB.com API to retrieve matching Internet Exchanges for the ASNs provided.

# Docker

Available as a container via docker hub.
```
https://hub.docker.com/r/locinetworks/peermyas
```
## Pull Docker container
```
docker pull locinetworks/peermyas
```

### Start container
```
docker run -d -p 80:5000 locinetworks/peermyas:latest
```
