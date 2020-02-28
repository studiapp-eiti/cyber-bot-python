from . import generic_scrapper, apache_scrapper, base_scrapper


class ScrapperCreator:
    SCRAPPERS = {"GenericScrapper": generic_scrapper.GenericScrapper,
                 "ApacheIndexesScrapper": apache_scrapper.ApacheIndexesScrapper}

    @classmethod
    def determine_scrapper(cls, scrapper_name):
        try:
            return cls.SCRAPPERS[scrapper_name]
        except KeyError as e:
            raise ValueError("Incorrect scrapper name provided!") from e

    @classmethod
    def from_json(cls, data: dict, subject_id: int) -> base_scrapper.Scrapper:
        scrapper_type = data["type"]
        scrapper_class = cls.determine_scrapper(scrapper_type)
        return scrapper_class(subject_id, data)
