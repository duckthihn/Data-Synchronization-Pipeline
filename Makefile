up:
	@docker compose up -d

down:
	@docker compose down

mysql-root:
	@docker exec -it mysql1 mysql -u root -p github_data

mysql-user:
	@docker exec -it mysql1 mysql -u myuser -p
