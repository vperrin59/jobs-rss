
gen_feeds:
	cd ./src && python main.py

deploy_feeds:
	git add ./feeds
	git commit -m "Update feed" || echo "No changes"
	git push