from src.Sofascore.SofascoreContainer import build_container


def main():
    # build_container() escolhe o transporte (browser por default) e tolera o Sofascore fora do ar.
    container = build_container()
    try:
        country = container.crawler.country_alpha(container.network)
        print(country)

        category = container.crawler.sport_categories_all(container.network, sport='football')
        print(category)
    finally:
        # com o transporte de browser isso encerra o Chromium; sem o close ele fica de pé.
        container.network.close()


if __name__ == '__main__':
    main()
