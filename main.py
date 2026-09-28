from src.Sofascore.SofascoreContainer import SofascoreContainer


def main():
    container = SofascoreContainer()
    country = container.crawler.country_alpha(container.network)
    print(country)

    category = container.crawler.sport_categories_all(container.network, sport='football')
    print(category)


if __name__ == '__main__':
    main()
