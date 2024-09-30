serve:
	docker-compose up -d --build
	docker compose logs -f backend

shell:
	docker compose run --rm backend python ./manage.py shell_plus --ipython

test:
	docker compose run --rm backend pytest
