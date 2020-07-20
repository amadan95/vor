from data import scrape_adp, scrape_projections

df = scrape_projections.scrape_projections()

df.to_csv('csv/projections.csv')