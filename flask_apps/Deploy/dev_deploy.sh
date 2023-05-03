docker network create bg_net 
&docker run -d --name elasticsearch --net bg_net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:8.7.1
&docker run --name bg_db -d -p 5432:5432 -e POSTGRES_PASSWORD=<your_pass> postgres:latest
