from src.Sofascore.SofascoreContainer import SofascoreContainer


def main():
    container = SofascoreContainer()
    country = container.crawler.country_alpha(container.network)
    print(country)


if __name__ == '__main__':
    main()
