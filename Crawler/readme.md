# Investing.com Crawler

## How to use
1. First, go to `settings.py` and scroll to the bottom. Config `ROOT_FOLDER`, `LOG_COUNTRY`, `LOG_COMPANY` and `LOG_STOCK`:

   `ROOT_FOLDER` is the absolute path to the InvestData directory.

   `LOG_COUNTRY`, `LOG_COMPANY` and `LOG_STOCK` are the relative paths to the files which the parsed response will be written to.

2. Run the following commands:
   ```
   scrapy crawl country
   scrapy crawl company
   scrapy crawl stock
   ```

3. The country list and company list should only be crawled once in a while. Stock can be crawled daily.

## Note

1. You can edit the `feed()` method in each spider to change the input.
2. You might encounter this error:
   ```
   [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <406 https://www.investing.com/equities/belgium>: HTTP status code is not handled or not allowed
   ```
   This means the server has blocked your access to this specific URL. You can continue crawling by using a VPN.