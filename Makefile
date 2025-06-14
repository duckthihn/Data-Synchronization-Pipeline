up:
	@docker compose -f docker/compose.yml up -d

down:
	@docker compose -f docker/compose.yml down

mysql:
	@docker exec -it mysql mysql -u root -p -D github_data

mongo:
	@docker exec -it mongodb mongosh -u duckthihn

redis:
	@docker exec -it redis redis-cli -a rootpassword