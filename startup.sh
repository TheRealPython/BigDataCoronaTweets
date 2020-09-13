docker network create kafka-network
docker-compose -f docker-compose.kafka.yml up -d
docker-compose up --scale web=2 -d
docker-compose -f docker-compose-spark.yml up -d
./build.sh
cd speed/
docker build -t bde/spark-app .
docker run --network=kafka-network --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false bde/spark-app
cd ..