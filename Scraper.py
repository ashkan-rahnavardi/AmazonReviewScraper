from requests_html import HTMLSession
import re


class Reviews:
    def __init__(self, product_url) -> None:
        self.product_url = product_url
        self.session = HTMLSession()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}

    def get_asin(self):
        """Returns the asin for the given amazon product URL"""
        asins = re.findall(r'/[dg]p/([^/]+)', self.product_url, flags=re.IGNORECASE)
        return asins[0]

    def pagination(self, page):
        """
        Returns the html for the product review page.

        :param page: the page number of the review page.
        :return: html if product reviews exist on given page, False if no reviews exist.
        """
        asin = self.get_asin()
        review_url = f'https://amazon.ca/product-reviews/{asin}/?pageNumber='  # URL for product review page
        r = self.session.get(review_url + str(page))
        r.html.render()
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook=review-title]', first=True).text
            rating = review.find('i[data-hook=review-star-rating] span', first=True).text
            body = review.find('span[data-hook=review-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'title': title,
                'rating': rating,
                'body': body
            }
            total.append(data)
        return total


if __name__ == '__main__':
    amz = Reviews('https://www.amazon.ca/Floating-OMOUBOI-Swimming-Snorkeling-Inflatable/dp/B08K32JFR7/ref=cm_cr_arp_d_product_top?ie=UTF8')
    all_reviews = []
    reviews_exist = True
    page_number = 1
    while reviews_exist:
        print('getting page ', page_number)
        reviews = amz.pagination(page_number)
        if reviews is not False:
            all_reviews.append(amz.parse(reviews))
            page_number += 1
        else:
            reviews_exist = False
            print('no more pages')
    print(all_reviews)
