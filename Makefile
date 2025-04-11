up:
	@docker compose -f docker/compose.yml up -d

down:
	@docker compose -f docker/compose.yml down

mysql:
	@docker exec -it mysql mysql -u root -p

mongo:
	@docker exec -it mongodb mongosh -u root -p

redis:
	@docker exec -it redis redis-cli