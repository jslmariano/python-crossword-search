#NOTE

docker-compose up -d --build
docker-compose logs -f
docker-compose exec -T app python --version
docker-compose exec -T app python WordSearch.py 10 5 add
docker-compose exec -T app python WordSearch.py puzzles/puzzle1.pzl
docker-compose exec -T app python test.py

docker-compose exec -T app coverage run test.py
docker-compose exec -T app coverage report
docker-compose exec -T app coverage html



