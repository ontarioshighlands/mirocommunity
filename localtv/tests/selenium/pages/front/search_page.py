"""Any page with the Search box for a video search.

"""

from localtv.tests.selenium.pages.front import MCFrontPage
import time


class SearchPage(MCFrontPage):
    """Search Page - lists the results of a search.

    """

    _SEARCH_RESULT_THUMB = '.tiles-item img'
    _SEARCH_RESULT_TITLE = '.grid-item-header h1'
    _SEARCH_RESULT_TIMESTAMP = '.grid-item-header p'
    _SEARCH_RESULT_LINK = '.grid-item-link'
    _SEARCH_HEADER = 'header.page-header h1'
    _RSS = 'a.rss'
    _NO_RESULTS = 'div#main h2'
    _NO_RESULTS_TEXT = ('Sorry, we could not find any videos matching '
                        'that query.')

    def on_searchable_page(self):
        """Open the home page if current page does not have search box.

        """
        if not self.is_element_present(self.SEARCH_BOX):
            self.open_page(self.base_url)

    def search(self, term):
        """Submit a search.

        """
        self.logger.info('Searching for %s' % term)
        self.on_searchable_page()
        self.clear_text(self.SEARCH_BOX)
        self.type_by_css(self.SEARCH_BOX, term)
        self.click_by_css(self.SEARCH_SUBMIT)

    def has_results(self, expected=True):
        """Verify search displays results, or No Results message if expected.

        """
        self.logger.info('Checking for search results')
        if not expected:
            time.sleep(5)
            if self.is_text_present(self._NO_RESULTS, self._NO_RESULTS_TEXT):
                return False, 'I am not expecting results'
            else:
                return True, 'Did not find the expected no results message'
        results = self._search_results()
        if results['titles'] > 0:
            return True, results
        else:
            return False, self.page_error()

    def click_first_result(self):
        """Click the thumb of the first result on the page.

        """
        self.logger.info('Clicking the first returned search result')
        self.wait_for_element_present(self._SEARCH_RESULT_THUMB)
        if not self.is_element_present(self._SEARCH_RESULT_THUMB):
            return False, 'There are no results on the page'
        vid_page = self.get_element_attribute(
            self._SEARCH_RESULT_LINK, 'href')
        self.click_by_css(self._SEARCH_RESULT_LINK)
        return True, vid_page

    def _search_results(self):
        """Return the number of thumbnails, titles and submitted dates.

        """
        result = {}
        thumbs = self.count_elements_present(self._SEARCH_RESULT_THUMB)
        titles = self.count_elements_present(self._SEARCH_RESULT_TITLE)
        times = self.count_elements_present(self._SEARCH_RESULT_TIMESTAMP)
        result = {'thumbs': thumbs,
                  'titles': titles,
                  'times': times,
                  }
        return result
