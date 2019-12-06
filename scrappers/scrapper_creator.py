from . import generic_scrapper, apache_scrapper


class ScrapperCreator:

    SCRAPPERS = {"GenericScrapper": generic_scrapper.GenericScrapper,
             "ApacheIndexesScrapper": apache_scrapper.ApacheIndexesScrapper}

    @classmethod
    def determine_scrapper(cls, scrapper_name):
        try:
            return cls.SCRAPPERS[scrapper_name]
        except KeyError as e:
            raise ValueError("Provided not correct scrappers name") from e


    @classmethod
    def from_json(cls, data: dict, subject_id):
        s_type = data["type"]
        root_urls = data["root_urls"]
        scrapper_class = cls.determine_scrapper(s_type)
        return scrapper_class(subject_id, root_urls)


