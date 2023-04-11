# Put any command that doesn't create a file here (almost all of the commands)
.PHONY: \
	chown \
	clear_cache \
	help \
	manage \
	migrate \
	migrations \
	shell \
	test \
	tests \
	usage \
	default_workers \
	scoring_workers \
	beat \
	update_requirements \

usage:
	@echo "Available commands:"
	@echo "chown.....................Change ownership of files to own user"
	@echo "clear_cache...............Clear Django's cache"
	@echo "help......................Display available commands"
	@echo "manage....................Run a Django management command"
	@echo "migrate...................Run Django migrations"
	@echo "migrations................Create Django migrations"
	@echo "shell.....................Run Django command line"
	@echo "test......................Run Django tests"
	@echo "tests.....................Run Django tests"
	@echo "usage.....................Display available commands"
	@echo "default_workers...........Start default workers"
	@echo "scoring_workers...........Start scoring workers"
	@echo "beat......................Start celery beat"
	@echo "update_requirements.......Update requirements file after adding a dependency"

chown:
	@docker-compose run --rm django chown -R "`id -u`:`id -u`" "/code/${ARGS}"

clear_cache:
	$(MAKE) manage ARGS="clear_cache ${ARGS}"

help:
	$(MAKE) usage

manage:
	@docker-compose run --rm ${OPTIONS} django python3 ${PYTHON_ARGS} manage.py ${ARGS}

migrate:
	$(MAKE) manage ARGS="migrate ${ARGS}"

migrations:
	$(MAKE) manage ARGS="makemigrations ${ARGS}"

shell:
	$(MAKE) manage ARGS="shell_plus ${ARGS}"

test:
	$(MAKE) manage ARGS="test fix_the_news${ARGS}"

tests:
	$(MAKE) test

default_workers:
	@docker-compose run --rm django celery -A fix_the_news worker -l info -Q celery

scoring_workers:
	@docker-compose run --rm django celery -A fix_the_news worker -l info -Q scoring

beat:
	@docker-compose run --rm django celery -A fix_the_news beat -l info

update_requirements:
	@docker-compose run --rm django pip freeze > requirements.txt
