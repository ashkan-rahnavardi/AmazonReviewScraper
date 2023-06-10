from requests_html import HTMLSession


class Reviews:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}
        self.url = f'https://www.amazon.ca/Floating-OMOUBOI-Swimming-Snorkeling-Inflatable/product-reviews/{self.asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        r.html.render(sleep=1)
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
    amz = Reviews('B08K32JFR7')
    reviews = amz.pagination(1)
    print(amz.parse(reviews))
